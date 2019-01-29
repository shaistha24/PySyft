import torch

from syft.frameworks.torch.tensors import PointerTensor


def test_overload_reshape():
    tensor = torch.Tensor([1, 2, 3, 4])
    tensor_reshaped = tensor.reshape((2, 2))
    tensor_matrix = torch.Tensor([[1.0, 2.0], [3.0, 4.0]])
    assert (tensor_reshaped == tensor_matrix).all()


def test_owner_default(hook):
    tensor = torch.Tensor([1, 2, 3, 4, 5])

    assert tensor.owner == hook.local_worker


def test_create_pointer(hook, workers):
    tensor = torch.Tensor([1, 2, 3, 4, 5])

    ptr = tensor.create_pointer(
        location=workers["bob"], id_at_location=1, register=False, owner=hook.local_worker, ptr_id=2
    )

    assert ptr.owner == hook.local_worker
    assert ptr.location == workers["bob"]
    assert ptr.id_at_location == 1
    assert ptr.id == 2

    ptr2 = tensor.create_pointer(owner=hook.local_worker)
    assert isinstance(ptr2.__str__(), str)
    assert isinstance(ptr2.__repr__(), str)


def test_create_pointer_defaults(workers):
    tensor = torch.Tensor([1, 2, 3, 4, 5])

    ptr = tensor.create_pointer(location=workers["bob"])

    assert ptr.owner == tensor.owner
    assert ptr.location == workers["bob"]


def test_get(workers):
    bob = workers["bob"]
    me = workers["me"]
    tensor = torch.rand(5, 3)
    tensor.owner = me
    tensor.id = 1

    pointer = tensor.send(bob)

    assert type(pointer.child) == PointerTensor
    assert (pointer.get() == tensor).all()