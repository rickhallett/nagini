class PythonExam:

    def test_list_comprehension(self):
        result = [x * 2 for x in range(5)]
        assert result == None

    def test_lambda_function(self):
        def square(x): return x ** 2
        assert square(5) == None

    def test_dictionary_comprehension(self):
        result = {k: k * 2 for k in range(1, 4)}
        assert result == None

    def test_set_operations(self):
        s1 = {1, 2, 3}
        s2 = {3, 4, 5}
        result = s1.intersection(s2)
        assert result == None

    def test_string_manipulation(self):
        result = 'hello'.upper()[::-1]
        assert result == None

    def test_generator_expression(self):
        result = sum(x * 2 for x in range(5))
        assert result == None

    def test_map_function(self):
        result = list(map(lambda x: x * 2, [1, 2, 3]))
        assert result == None

    def test_zip_function(self):
        result = list(zip([1, 2, 3], ['a', 'b', 'c']))
        assert result == None


if __name__ == '__main__':
    exam = PythonExam()
    exam.test_list_comprehension()
    exam.test_lambda_function()
    exam.test_dictionary_comprehension()
    exam.test_set_operations()
    exam.test_string_manipulation()
    exam.test_generator_expression()
    exam.test_map_function()
    exam.test_zip_function()
