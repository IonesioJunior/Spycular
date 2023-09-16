def test_new_class_instance(producer, consumer, replies):
    obj = producer.FatherClass(var1=35, var2="hello")
    var1_ptr = obj.var1
    var2_ptr = obj.var2

    var1_ptr.retrieve()
    var2_ptr.retrieve()
    consumer.listen()
    assert replies[var1_ptr.id] == 35
    assert replies[var2_ptr.id] == "hello"


def test_set_class_attributes(producer, consumer, replies):
    obj = producer.FatherClass(var1=35, var2="hello")
    var1_ptr = obj.var1
    var2_ptr = obj.var2
    var1_ptr.retrieve()
    var2_ptr.retrieve()
    consumer.listen()
    assert replies[var1_ptr.id] == 35
    assert replies[var2_ptr.id] == "hello"
    obj.var1 = 27
    obj.var2 = "world"
    new_var1 = obj.var1
    new_var2 = obj.var2
    new_var1.retrieve()
    new_var2.retrieve()
    consumer.listen()
    assert replies[new_var1.id] == 27
    assert replies[new_var2.id] == "world"


def test_call_class_method(producer, consumer, replies):
    obj = producer.FatherClass(var1=35, var2="hello")
    obj.increment(2)
    new_var1 = obj.var1
    new_var1.retrieve()
    consumer.listen()
    assert replies[new_var1.id] == 37


def test_call_class_method_2(producer, consumer, replies):
    obj = producer.FatherClass(var1=35, var2="hello")
    ptr = obj.give_length()
    ptr.retrieve()
    consumer.listen()
    assert replies[ptr.id] == 5


def test_class_extends(producer, consumer, replies):
    class ChildClass(producer.FatherClass.__class__):
        def __init__(self, var1, var2):
            super().__init__(
                super_pointer=producer.FatherClass,
                var1=var1,
                var2=var2,
            )

        def child_method(self):
            self.increment(2)
            return self.var1 + self.give_length()

    obj = ChildClass(var1=35, var2="hello")
    ptr = obj.child_method()
    ptr.retrieve()
    consumer.listen()
    assert replies[ptr.id] == 42
