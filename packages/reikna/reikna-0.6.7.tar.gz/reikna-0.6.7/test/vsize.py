import itertools

from reikna.cluda import ocl_api, cuda_api
from reikna.cluda import OutOfResourcesError
import reikna.cluda.vsize as vsize
from reikna.helpers import min_blocks, product
import reikna.cluda.dtypes as dtypes
from helpers import *

from pytest_threadgen import parametrize_thread_tuple, create_thread_in_tuple


class ReferenceIds:

    def __init__(self, global_size, local_size):
        self.global_size = global_size
        if local_size is not None:
            self.local_size = local_size
            self.grid_size = tuple(min_blocks(gs, ls) for gs, ls in zip(global_size, local_size))

    def _tile_pattern(self, pattern, axis, full_shape):

        pattern_shape = [x if i == axis else 1 for i, x in enumerate(full_shape)]
        pattern = pattern.reshape(*pattern_shape)

        tile_shape = [x if i != axis else 1 for i, x in enumerate(full_shape)]
        pattern = numpy.tile(pattern, tile_shape)

        return pattern.astype(numpy.int32)

    def predict_local_ids(self, dim):
        global_len = self.global_size[dim]
        local_len = self.local_size[dim]
        repetitions = min_blocks(global_len, local_len)

        pattern = numpy.tile(numpy.arange(local_len), repetitions)[:global_len]
        return self._tile_pattern(pattern, dim, self.global_size)

    def predict_group_ids(self, dim):
        global_len = self.global_size[dim]
        local_len = self.local_size[dim]
        repetitions = min_blocks(global_len, local_len)

        pattern = numpy.repeat(numpy.arange(repetitions), local_len)[:global_len]
        return self._tile_pattern(pattern, dim, self.global_size)

    def predict_global_ids(self, dim):
        global_len = self.global_size[dim]

        pattern = numpy.arange(global_len)
        return self._tile_pattern(pattern, dim, self.global_size)


class TestVirtualSizes:

    @classmethod
    def try_create(cls, global_size, local_size, max_num_groups, max_work_item_sizes):
        """
        This method is used to filter working combinations of parameters
        from the cartesian product of all possible ones.
        Returns ``None`` if the parameters are not compatible.
        """
        if len(max_num_groups) != len(max_work_item_sizes):
            return None

        if local_size is not None:
            if len(local_size) > len(global_size):
                return None
            else:
                # we need local size and global size of the same length
                local_size = local_size + (1,) * (len(global_size) - len(local_size))

            if product(local_size) > product(max_work_item_sizes):
                return None

            bounding_global_size = [
                ls * min_blocks(gs, ls) for gs, ls
                in zip(global_size, local_size)]

            if product(bounding_global_size) > product(max_num_groups):
                return None

        else:
            if product(global_size) > product(max_num_groups):
                return None

        return cls(global_size, local_size, max_num_groups, max_work_item_sizes)

    def __init__(self, global_size, local_size, max_num_groups, max_work_item_sizes):
        self.global_size = global_size
        self.local_size = local_size
        if local_size is not None:
            self.grid_size = tuple(min_blocks(gs, ls) for gs, ls in zip(global_size, local_size))

        self.max_num_groups = max_num_groups
        self.max_work_item_sizes = max_work_item_sizes

    def is_supported_by(self, thr):
        return (
            len(self.max_num_groups) <= len(thr.device_params.max_num_groups) and
            all(ng <= mng for ng, mng
                in zip(self.max_num_groups, thr.device_params.max_num_groups)) and
            len(self.max_work_item_sizes) <= len(thr.device_params.max_work_item_sizes) and
            all(wi <= mwi for wi, mwi
                in zip(self.max_work_item_sizes, thr.device_params.max_work_item_sizes)))

    def __str__(self):
        return "{gs}-{ls}-limited-by-{mng}-{mwis}".format(
            gs=self.global_size, ls=self.local_size,
            mng=self.max_num_groups, mwis=self.max_work_item_sizes)


class override_device_params:
    """
    Some of the tests here need to make thread/workgroup number limits
    in DeviceParameters of the thread lower, so that they are easier to test.

    This context manager hacks into the Thread and replaces the ``device_params`` attribute.
    Since threads are reused, the old device_params must be restored on exit.
    """

    def __init__(self, thr, **kwds):
        self._thr = thr
        self._kwds = kwds

    def __enter__(self):
        self._old_device_params = self._thr.device_params
        device_params = self._thr.api.DeviceParameters(self._thr._device)
        for kwd, val in self._kwds.items():
            setattr(device_params, kwd, val)
        self._thr.device_params = device_params
        return self._thr

    def __exit__(self, *args):
        self._thr.device_params = self._old_device_params


if __name__ == '__main__':

    api = ocl_api()
    thr = api.Thread(api.get_platforms()[0].get_devices()[1])

    testvs = TestVirtualSizes.try_create(
        global_size=(5, 33, 75),
        local_size=None,
        max_num_groups=(34, 56, 25),
        max_work_item_sizes=(9, 5, 3))
    ref = ReferenceIds(testvs.global_size, testvs.local_size)
    with override_device_params(
            thr, max_num_groups=testvs.max_num_groups,
            max_work_item_sizes=testvs.max_work_item_sizes, warp_size=3) as limited_thr:

        get_ids = limited_thr.compile_static("""
        KERNEL void get_ids(
            GLOBAL_MEM int *local_ids,
            GLOBAL_MEM int *group_ids,
            GLOBAL_MEM int *global_ids,
            int vdim)
        {
            VIRTUAL_SKIP_THREADS;
            const VSIZE_T i = virtual_global_flat_id();
            local_ids[i] = virtual_local_id(vdim);
            group_ids[i] = virtual_group_id(vdim);
            global_ids[i] = virtual_global_id(vdim);
        }
        """, 'get_ids', testvs.global_size, local_size=testvs.local_size)

        print(testvs.global_size, testvs.local_size)

        print(get_ids.global_size)
        print(get_ids.local_size)
        print(get_ids.virtual_global_size)
        print(get_ids.virtual_local_size)
        print(get_ids._program.source)

    local_ids = thr.array(ref.global_size, numpy.int32)
    group_ids = thr.array(ref.global_size, numpy.int32)
    global_ids = thr.array(ref.global_size, numpy.int32)

    for vdim in range(len(testvs.global_size)):

        get_ids(local_ids, group_ids, global_ids, numpy.int32(vdim))

        print(vdim)

        assert diff_is_negligible(global_ids.get(), ref.predict_global_ids(vdim))
        if testvs.local_size is not None:
            assert diff_is_negligible(local_ids.get(), ref.predict_local_ids(vdim))
            assert diff_is_negligible(group_ids.get(), ref.predict_group_ids(vdim))
