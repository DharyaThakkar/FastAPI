#Here we will create tests for each new file according to naming convention :-
#   'test_<file_name>'

import pytest

def test_equal_or_not_equal(): #we can have more than one assert test in one function.Both conditions must be passed to make sure that the test is actually passed.
    assert 3 == 3 #True
    assert 3 != 1 #True


def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10',int)
    
def test_boolean():
    validated = True
    assert validated is True
    assert('hello' == 'world') is False
    
     
def test_type():
    assert type('Hello' is str)
    assert type('World' is not int)
    
def test_greater_and_less_than():
    assert  7 > 3
    assert  4 < 10
 
def test_list():
    num_list = [1,2,3,4,5]
    any_list = [False,False]
    
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)              
    

class Student:
    def __init__(self,first_name:str, last_name:str, major:str, years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
   
  
  
@pytest.fixture
def default_employee():
    return Student('John', 'Doe', 'Computer Science', 3)

      
        
def test_person_initialization(default_employee): #using pytest fixture as an parameter which will help us create Student object automatically.
    
    # p = Student('John', 'Doe', 'Computer Science', 3) #we are instantiating new object in the test, and we have to do every single time if we want to use the properties of that object.
    #so if we do not want to instantiate a new object every single time we are going to test against, then we can use something called as pytest fixture.it wil help us to instantiate an object and then pass it into our test function and this happens automatically behind the scenes.
    
    assert default_employee.first_name =='John', 'First name should be John'
    assert default_employee.last_name == 'Doe','Last name should be Doe'
    assert default_employee.major == 'Computer Science'
    assert default_employee.years == 3
     
    