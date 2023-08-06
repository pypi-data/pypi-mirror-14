Overdub
=======

Load and merge nested configurations.


Usage
-----

Installation::

    python -m pip install overdub


With these structures::

    from overdub import MutableOverdub

    a = {'foo': 1, 'bar': {'baz': 2}, 'qux': {'one': 1}}
    b = {'foo': 3, 'bar': {'baz': 4}, 'qux': {'two': 2}}

Update::

    overdubbed = MutableOverdub(a)
    overdubbed.update(b)
    assert overdubbed.foo == 3
    assert overdubbed.bar.baz == 4
    assert overdubbed.qux == {'two': 2}


Merge::

    overdubbed = MutableOverdub(a)
    overdubbed.merge(b)
    assert overdubbed.foo == 3
    assert overdubbed.bar.baz == 4
    assert overdubbed.qux == {'one': 1, 'two': 2}


Rebase::

    overdubbed = MutableOverdub(a)
    overdubbed.rebase(b)
    assert overdubbed.foo == 1
    assert overdubbed.bar.baz == 2
    assert overdubbed.qux == {'one': 1, 'two': 2}


Unbound the data::

    overdubbed = MutableOverdub(a)
    assert isinstance(overdubbed, Overdub)
    naked = MutableOverdub(a)
    assert not isinstance(naked, Overdub)


Freeze configuration::

    overdubbed = overdubbed.frozen()


YAML files
----------

It can also read configuration from yaml files, for this install::

    python -m pip install overdub[yaml]

And then, merge all files::

    from overdub import yaml

    overdubbed = yaml.load_from_file('a.yml', b.yml')
    assert overdubbed.foo == 3
    assert overdubbed.bar.baz == 4
    assert overdubbed.qux == {'one': 1, 'two': 2}
