import numpy

from reikna.cluda import ocl_api, cuda_api

api = cuda_api()
thr = api.Thread(api.get_platforms()[0].get_devices()[0])


get_ids = thr.compile("""

WITHIN_KERNEL VSIZE_T virtual_local_id(unsigned int dim)
{
    if (dim == 2)
    {
        SIZE_T flat_id =
            get_local_id(0) * 1 +
            get_local_id(1) * 9 +
            get_local_id(2) * 45 +
            0;

        return (flat_id / 1);
    }
    if (dim == 1)
    {
        SIZE_T flat_id =
            get_local_id(3) * 1 +
            0;

        return (flat_id / 1) % 1;
    }
    if (dim == 0)
    {
        SIZE_T flat_id =
            get_local_id(3) * 1 +
            0;

        return (flat_id / 1);
    }

    return 0;
}

WITHIN_KERNEL VSIZE_T virtual_local_size(unsigned int dim)
{
    if (dim == 2)
    {
        return 134;
    }
    if (dim == 1)
    {
        return 1;
    }
    if (dim == 0)
    {
        return 1;
    }

    return 1;
}

WITHIN_KERNEL VSIZE_T virtual_group_id(unsigned int dim)
{
    if (dim == 2)
    {
        SIZE_T flat_id =
            get_group_id(0) * 1 +
            0;

        return (flat_id / 1) % 1;
    }
    if (dim == 1)
    {
        SIZE_T flat_id =
            get_group_id(0) * 1 +
            0;

        return (flat_id / 1);
    }
    if (dim == 0)
    {
        SIZE_T flat_id =
            get_group_id(1) * 1 +
            0;

        return (flat_id / 1);
    }

    return 0;
}

WITHIN_KERNEL VSIZE_T virtual_num_groups(unsigned int dim)
{
    if (dim == 2)
    {
        return 1;
    }
    if (dim == 1)
    {
        return 33;
    }
    if (dim == 0)
    {
        return 5;
    }

    return 1;
}

WITHIN_KERNEL VSIZE_T virtual_global_id(unsigned int dim)
{
    return virtual_local_id(dim) + virtual_group_id(dim) * virtual_local_size(dim);
}

WITHIN_KERNEL VSIZE_T virtual_global_size(unsigned int dim)
{
    if(dim == 2)
    {
        return 75;
    }
    if(dim == 1)
    {
        return 33;
    }
    if(dim == 0)
    {
        return 5;
    }

    return 1;
}

WITHIN_KERNEL VSIZE_T virtual_global_flat_id()
{
    return
        virtual_global_id(2) * 1 +
        virtual_global_id(1) * 75 +
        virtual_global_id(0) * 2475 +
        0;
}

WITHIN_KERNEL VSIZE_T virtual_global_flat_size()
{
    return
        virtual_global_size(2) *
        virtual_global_size(1) *
        virtual_global_size(0) *
        1;
}


WITHIN_KERNEL bool virtual_skip_local_threads()
{
    {
        VSIZE_T flat_id =
            get_local_id(0) * 1 +
            get_local_id(1) * 9 +
            get_local_id(2) * 45 +
            0;

        if (flat_id >= 134)
            return true;
    }

    return false;
}

WITHIN_KERNEL bool virtual_skip_groups()
{

    return false;
}

WITHIN_KERNEL bool virtual_skip_global_threads()
{
    if (virtual_global_id(2) >= 75)
        return true;

    return false;
}

#define VIRTUAL_SKIP_THREADS if(virtual_skip_local_threads() || virtual_skip_groups() || virtual_skip_global_threads()) return


KERNEL void get_ids(
    GLOBAL_MEM int *local_ids,
    GLOBAL_MEM int *group_ids,
    GLOBAL_MEM int *global_ids,
    int vdim)
{
    VIRTUAL_SKIP_THREADS;

    const VSIZE_T i =
        (virtual_local_id(2) + virtual_group_id(2) * 134) * 1 +
        (virtual_local_id(1) + virtual_group_id(1) * 1) * 75 +
        (virtual_local_id(0) + virtual_group_id(0) * 1) * 2475 ;

    local_ids[i] = virtual_local_id(vdim);
    group_ids[i] = virtual_group_id(vdim);

    global_ids[
        /*
        (
            get_group_id(2) * 33 * 5
            + get_group_id(1) * 5
            + get_group_id(0)
            ) * 9 * 5 * 3
        + get_local_id(2) * 9 * 5
        + get_local_id(1) * 9
        + get_local_id(0)
        */
        i
        //get_global_id(2) * 297 * 25
        //+ get_global_id(1) * 297
        //+ get_global_id(0)

        ] = i;
}
    """).get_ids

global_size = (297, 25, 3)
local_size = (9, 5, 3)

local_ids = thr.to_device(numpy.ones((5, 33, 75), numpy.int32) * (-1))
group_ids = thr.to_device(numpy.ones((5, 33, 75), numpy.int32) * (-1))
global_ids = thr.to_device(numpy.ones((5, 33, 75), numpy.int32) * (-1))

vdim = 0
get_ids(local_ids, group_ids, global_ids, numpy.int32(vdim),
    global_size=global_size, local_size=local_size)

print(vdim)
print(global_ids.get()[0,0])
print(global_ids.get()[0,1])
print(global_ids.get()[0,2])
