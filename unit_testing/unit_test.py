import os
import click
import project.script as script

def test_validation():
    import os
    dir = os.path.dirname(os.path.abspath(__file__))

    #Expected inputs
    task = script.Task("name", dir+r"\project\script.py", "100", "P10H", True)
    assert task.validate()

    task = script.Task("name", dir+r"\unit_testing\file.exe", "1000", "P30D12H5M", True)
    assert task.validate()

    task = script.Task("name", dir+r"\project\script.py", "2", "P2M", True)
    assert task.validate()

    #Invalid path to program (expected false)
    task = script.Task("name", dir+r"\project\file.exe", "100", "P10H2M", True)
    assert not task.validate()

    #Invalid interval (expected false)
    task = script.Task("name", dir+r"\project\script.py", "a", "P10H2M", True)
    assert not task.validate()

    task = script.Task("name", dir+r"\project\script.py", "-14", "P10H2M", True)
    assert not task.validate()

    task = script.Task("name", dir+r"\project\script.py", "0", "P10H2M", True)
    assert not task.validate()

    #Invalid duration (expected false)
    task = script.Task("name", dir+r"\project\script.py", "100", "asdf", True)
    assert not task.validate()

    task = script.Task("name", dir+r"\project\script.py", "100", "4", True)
    assert not task.validate()

    #Interval greater than duration error (expected fail)
    task = script.Task("name", dir+r"\project\script.py", "200", "P2M", True)
    assert not task.validate()

if __name__ == '__main__':
    test_validation()