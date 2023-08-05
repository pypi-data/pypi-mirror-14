json2rust
=========

Turns a JSON document into a struct for rust-lang

Installation
------------

From the project root directory::

    $ python setup.py install

Or::
    
    $ pip install json2rust

Usage
-----

Simply run it with the name of the root struct and the path to your JSON::

    $ json2rust MyStruct data.json

Use --help/-h to view info on the arguments::

    $ json2rust --help

Example
-------

Take your JSON doc::

	$ cat testdata/example.json 
	{
		"name": "Me",
		"age": 33,
		"children": [
			{
				"name": "joe",
				"age": 0.5,
				"exists": false
			}
		],
		"job": {
			"employer": "foo",
			"salary": 5000000,
			"coworker": null
		}
	}

Run json2rust::

	$ json2rust ExampleStruct testdata/example.json 
	pub struct ExampleStruct {
		pub job: Job,
		pub age: i32,
		pub name: String,
		pub children: Vec<Children>,
	}
	pub struct Job {
		pub salary: i32,
		pub coworker: Option<UNKNOWN_NULL>,
		pub employer: String,
	}
	pub struct Children {
		pub age: f32,
		pub name: String,
		pub exists: bool,
	}

Release Notes
-------------

:0.1.0:
    Project works
:0.0.1:
    Project created
