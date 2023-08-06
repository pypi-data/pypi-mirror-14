Trust provides a caller with information stored in a JSON file, multiple JSON files or MongoDB database. By allowing JSON objects to refer to other JSON objects, Trust is a convinient way to access data while ensuring no data duplication exists. A single piece of data, such as an IP number, a price or a list of records, is stored in a single location and may be refered to by other objects in a transparent way for the caller.

Trust is also a way to secure data and audit data access. This makes it particularly valuable for storing configuration containing sensitive pieces, such as passwords.

Trust is a sort of an hierarchical database engine with read-only data access. Trust only queries the data and never changes it, which means that it is intended to be used for cases such as application configuration or infrastructure description, and not for situations where the application accessing the data will also change it.

Let's see how it works:

  - The section [Getting started](#head-getting-started) describes the first steps in using the library both locally and as a web service.

  - The sections [Queries](#head-queries) and [Inheritance](#head-inheritance) describe how Trust is used in practice, in other words how data is actually queried.

  - The section [Clients](#head-clients) and [Security](#head-security) explain how to deploy and configure Trust either locally or as a service.

  - The section [Contribute](#head-contribute) contains the information you need if you want to participate to the project or need technical support.

<h2 id="head-terms">Terms</h2>

**Object**: as opposed to value, a object is a part of which is enclosed in curly braces.

**Value**: as opposed to object, a value is either a scalar value such as a string, a number or a boolean, or an array of values or objects.

**Fork**: a case where JSON file has the same name (ignoring extension) than a directory within the same parent. see Queries, Forks.

<h2 id="head-getting-started">Getting started</h2>

If you're reading this documentation on GitHub, you probably know how to get the source. Otherwise, you can get it from our own SVN server by executing:

    svn checkout http://source.pelicandd.com/infrastructure/trust/

Now create a directory where data will be stored, for instance `/tmp/trust-data`. Inside, create a file called `example.json` with the following contents:

    {
        "hello": "Hello, World!"
    }

Go to the application directory and run the local client:

    python3 localtrust.py /tmp/trust-data /example/hello

You should be able to see "Hello, World!". The [next section](#head-queries) explains how to make queries go beyond the boring hello world.

If you want to use the web service, than you should be interested by `app/trust_blueprint.py` file. This is a Flask blueprint file which you can add to your Flask application. If you have no idea what a blueprint is, `server.py` contains an example. Another example is `website.py` which corresponds to [the actual site presenting the web service](http://services.pelicandd.com/trust/).

If you want to host the web service as a standalone web application, without integrating it to an existent website, use `server.py`. For instance, it can be hosted with Gunicorn using the following command:

    gunicorn server:flaskApp -b :80 -w 4 --log-syslog

<h2 id="head-queries">Queries</h2>

When accessing Trust data, the underlying data source is abstracted away from the caller. The data may be in a single JSON file, multiple JSON files, MongoDB documents, or something else.

This means that, when working with underlying JSON files, Trust will use the query to determine both the concerned file and the node within the file itself.

The structure of the data being hierarchical, the query looks like a path traversing the nodes from the root down to a leaf (or a non-leaf node).

The query may lead to either an object or a value. The original JSON is parsed, which means that the resulting objects or values are not necessarily written in the same way they were originally written, but in a way a JSON serializer will write them. For instance, note the dropped trailing zero in the price in the illustrations below.

*Illustration 1: query of an object*

  - **illustration1/example.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90
            }
        }

  - **Result for `/illustration1/example/product`**

        {
            "name": "Demo product",
            "price": 29.9
        }

If it is a value, it is returned as is, without being enclosed in curly braces.

*Illustration 2: query of a value*

  - **illustration2/example.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90
            }
        }

  - **Result for `/illustration2/example/product/price`**

        29.9

Arrays are considered values too, which means they don't have curly braces either. Arrays can contain values or objects.

*Illustration 3: query of an array*

  - **illustration3/example.json**

        {
            "products": [
                {
                    "name": "Demo product",
                    "price": 29.90
                },
                {
                    "name": "Second product",
                    "price": 16.00
                }
            ]
        }

  - **Result for `/illustration3/example/products`**

        [
            {
                "name": "Demo product",
                "price": 29.9
            },
            {
                "name": "Second product",
                "price": 16.0
            }
        ]

Since the underlying data source is not important, a query may return multiple files when data is stored in JSON files. Those files are combined following the file system hieararchy, the names of directories and files being used as keys in the resulting JSON:

*Illustration 4: getting multiple files at once*

  - **illustration4/first.json**

        {
            "say-hello": "Hello, World!"
        }

  - **illustration4/sub/second.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90
            }
        }

  - **Result for `/illustration4`**

        {
            "first": {
                "say-hello": "Hello, World!"
            },
            "sub": {
                "second": {
                    "product": {
                        "name": "Demo product",
                        "price": 29.90
                    }
                }
            }
        }

<h3 id="head-forks">Forks</h3>

It may happen that either the name of the file (ignoring the extension) is the same as the name of a directory within the same parent directory. We call this a fork.

In a case of a collision between JSON contents and directory hierarchy, only the JSON contents are taken and directory hierarchy is ignored. This is done to ensure consistency. Let's see how it works on an example:

*Illustration 5: fork resolution*

  - **illustration5/demo.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90
            }
        }

  - **illustration5/demo/product.json**

        {
            "description": "This is a product used for demo purposes."
        }

  - **Result for `/illustration5/demo/product`**

        {
            "name": "Demo product",
            "price": 29.90
        }

The situation is necessarily ambiguous: should we use `demo.json`, `product.json` or both? Since `demo.json` is the first one appearing through the hierarchy, it looks natural to use `demo.json`. Merging, in this situation, is problematic, because a person editing the JSON file may be unaware of other data through the hierarchy. To avoid this source of error, the directory hierarchy is ignored.

Note that with the current data, there is no way to read the description. For instance, the query for `/illustration5/demo/product/description` will produce the same result as when querying for a non-existent piece of data.

Back to consistency, let's query data a few levels above:

  - **Result for `/illustration5`**

        {
            "demo": {
                "product": {
                    "name": "Demo product",
                    "price": 29.90
                }
            }
        }

Description doesn't appear here either; otherwise, the results will be highly inconsistent: we'll get product description, but when requesting for product specifically, the description would disappear.

When fork is encountered, a warning is issued. It is crucial to show a warning, because the behavior may lead to inexpected results. As in most systems, warnings should be avoided. In Trust, data architects are expected to avoid forks by naming directories and files in a way they don't collide with JSON data.

<h3 id="head-query-formatting">Query formatting</h3>

The tree is traversed using a slash (`/`) character. Every step in the path query contains one or more Unicode characters. Although any Unicode class is allowed, the underlying data sources may be more limitative. In order to simplify later migration of data from one data source to another, data architects are invited to consider the limitations of all the concerned data sources.

A query always starts with a slash (`/`) and may contain nothing more than a slash (which will query for everything .

Queries are case insensitive and lowercased before reaching the data source. In operating systems such as Linux where file names are case sensitive, all files involved in querying should have lowercase characters.

The characters `.` (a dot) and `:` (a colon) receive special treatment. For instance, `/example/.keys` will return an array containing the keys of `/example` object:

*Illustration 6: retrieving object keys*

  - **illustration6/example.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90
            }
        }

  - **Result for `/illustration6/example/product/.keys`**

        [
            "name",
            "price"
        ]

while `/example/.plain:.keys` will return an object or a value corresponding to `/example/.keys`. If the `.plain:` part appears several times, only the first one is used.

*Illustration 7: escaping*

  - **illustration7/example.json**

        {
            "product": {
                "name": "Demo product",
                "price": 29.90,
                ".plain:.plain:.keys": "Hello, World!"
            }
        }

  - **Result for `/illustration7/example/product/.plain:.plain:.plain:.keys`**

        "Hello, World!"

A step cannot be `.` or `..`, including when the data source is not a file system. The reason for that is that it's easier and safer to block such steps early, and should not be an important limitation for data architects (if you're really actually calling your nodes `.` and `..`, you may reconsider your naming conventions).

Note that quotes (`"`) are valid in query paths.

The encoding used by Trust is UTF-8 for both the query and the underlying data. Trust is expected to support the full Unicode range of characters, although some underlying data sources may not be able to accept some characters due to their specific constraints.

<h2 id="head-inheritance">Inheritance</h2>

Inheritance is the mecanism used by Trust to eliminate data duplication.

Inheritance consists for a node (a child) to refer to another node (a parent). The child and the parent can then be combined using different rules described below. Those rules are different whether they involve objects or values (see [Terms](#head-terms)).

The inheritance is done with the statement `.special:inherit`.

<h3 id="head-inheritance-involving-objects">Inheritance involving objects</h3>

When an object inherits another one, the default behavior is to merge them. For instance, if JSON files are describing machines, another file may contain global settings used for every machine.

*Illustration 8: default object inheritance*

  - **illustration8/common.json**

        {
            "network": {
                "dns": "192.168.1.2"
            }
        }

  - **illustration8/http-server.json**

        {
            ".special:inherit": "/illustration8/common",
            "network": {
                "ip": "192.168.1.113"
            }
        }

  - **Result for `/illustration8/http-server`**

        {
            "network": {
                "ip": "192.168.1.113",
                "dns": "192.168.1.2"
            }
        }

It is also possible to replace the child node by the parent node. For instance, let's imagine two JSON objects: one describes a DNS machine; another one describes another machine which needs to access DNS server.

*Illustration 9: object inheritance with replacement*

  - **illustration9/dns-machine.json**

        {
            "network": {
                "ip": "192.168.1.2"
            }
        }

  - **illustration9/http-server.json**

        {
            "network": {
                "ip": "192.168.1.113",
                "dns": {
                    ".special:inherit": "/illustration9/dns-machine/network/ip",
                    ".special:actions": ["replace"]
                }
            }
        }

  - **Result for `/illustration9/http-server`**

        {
            "network": {
                "ip": "192.168.1.113",
                "dns": "192.168.1.2"
            }
        }

<h3 id="head-inheritance-involving-values">Inheritance involving values</h3>

Values are simply overwritten, that is child values replace values from parent when applying inheritance.

*Illustration 10: inheritance involving values*

  - **illustration10/parent.json**

        {
            "say-hello": "Hello",
            "numbers": [5, 1, 1, 3]
        }

  - **illustration10/child.json**

        {
            ".special:inherit": "/illustration10/parent",
            "say-hello": "Hello, World",
            "numbers": [2, 3, 7, 7]
        }

  - **Result for `/illustration10/child`**

        {
            "say-hello": "Hello, World",
            "numbers": [2, 3, 7, 7]
        }

Dealing with arrays is slightly different. While the default behavior is replacement, exactly as with the non-array values, other actions can be applied. Arrays may be extended by specifying either `add` or `merge` in `.special:actions`.

Arrays addition produces an array which contains all the elements of the parent array and all the elements of the child array. If an element exists in both the parent and the child array, it will appear twice in the resulting array.

*Illustration 11: inheritance involving arrays addition*

  - **illustration11/parent.json**

        {
            "numbers": [5, 1, 1, 3]
        }

  - **illustration11/child.json**

        {
            ".special:inherit": "/illustration11/parent",
            "numbers": {
                ".special:actions": ["add"],
                ".special:values": [2, 3, 7, 7]
            }
        }

  - **Result for `/illustration11/child/numbers`**

        [5, 1, 1, 3, 2, 3, 7, 7]

The merge mode is very different. Not only it takes only once an element which appears in both the child and the parent array, but **it also removes duplicate elements within the child and within the parent**. It is like using an addition and then selecting unique elements only. Moreover, **the results are sorted**.

*Illustration 12: inheritance involving arrays merging*

  - **illustration12/parent.json**

        {
            "numbers": [5, 1, 1, 3]
        }

  - **illustration12/child.json**

        {
            ".special:inherit": "/illustration12/parent",
            "numbers": {
                ".special:actions": ["merge"],
                ".special:values": [2, 3, 7, 7]
            }
        }

  - **Result for `/illustration12/child/numbers`**

        [1, 2, 3, 5, 7]

<h3 id="head-circular-inheritance">Prevention of circular inheritance</h3>

The circular inheritance is prevented by disallowing to inherit from an element which is already in the inheritance chain. This means that it applies both to the situation where the node inherits from itself (or nodes which contain itself) and the one where two nodes inherit from each other.

*Illustration 27: circular inheritance on a single node*

 - **illustration27/example.json**:

        {
            "hello": "Hello, World!",
            "infinite": {
                ".special:inherit": "/illustration27/example"
            }
        }

 - **Result for illustration27/example**:

        "errors": [
            {
                "type": "circular-inheritance",
                "uri": "http://services.pelicandd.com/trust/error/circular-inheritance",
                "description": "The data contains a circular inheritance."
            }
        ]

*Illustration 29: circular inheritance involving multiple nodes*

 - **illustration29/example.json**:

        {
            "hello": "Hello, World!",
            "first": {
                ".special:inherit": "/illustration29/example/second"
            },
            "second": {
                ".special:inherit": "/illustration29/example/first"
            }
        }

 - **Result for illustration29/example**:

        "errors": [
            {
                "type": "circular-inheritance",
                "uri": "http://services.pelicandd.com/trust/error/circular-inheritance",
                "description": "The data contains a circular inheritance."
            }
        ]
<h2 id="head-clients">Clients</h2>

Trust comes in two forms: a script and an API.

<h3 id="head-script">Script</h3>

A script is a Python 3 application which can be used locally to access locally data stored in files, on NFS or in MongoDB.

**Synopsis**

    python3 trust.py [-h] [--optional] [--source source] [--response-mode json|complete|text] [--username username [--password password]] query

**Arguments**

  - `--response-mode` argument specifies how the response is formatted and can accept one of the following values:

     1. `json` (default): the object or the value are returned directly using JSON format. Every example above uses this mode.

     2. `complete`: the result is a complex JSON object which contains not only the object or the value, both enclosed in `result` object, but also eventual warnings and errors. An example of a response may be:

            {
                "result": {
                    "product": {
                        "name": "Demo product",
                        "price": 29.9
                    }
                },
                "warnings": [
                    {
                        "message": "A fork is found at the specified path. One tine only will be used.",
                        "path": "/example/demo"
                    }
                ]
            }

     3. `text`: the mode is similar to `json`; the only difference appears when the result is an array. In this case, instead of returning its JSON representation, each element of the array is returned on a separate line. This may be useful when processing a response in `bash`. Note that arrays within objects or other arrays are still serialized to JSON.

  - `--optional`: indicates that if the object or value corresponding to the query doesn't exist, Trust should return nothing instead of throwing an exception. If the response mode is set to `complete`, the response will be:

            {
                "result": null
            }

    If the response mode is set to `json` or `text`, the response will be zero-length stream.

  - `--source` argument indicates where the data should be found. It may be a connection string to a MongoDB database, in which case it should start with `mongodb://` (see [Connection String URI Format](http://docs.mongodb.org/manual/reference/connection-string/)). Or it may be an absolute path to a single JSON file or a directory containing JSON files.

  - `--username` argument, combined with `--password`, provide the application with credentials which will be used to grant access to parts which are otherwise restricted. See [Security](#head-security) for more information.

<h3 id="head-api">API</h3>

(This section is incomplete. The API is not done yet.)

<h3 id="head-warnings">Warnings and errors</h3>

When calling the script, warnings and errors are logged to syslog. If the caller specifies `complete` response mode (see response modes above), the warnings and errors are also enclosed within the response.

<h2 id="head-security">Security</h2>

Some pieces of data can be restricted to some users or groups of users.

Trust has a default authentication provider, but other providers can be developed and injected in Trust when called through Python. In order to work, a credentials provider should be a Python class which has the following methods:

    def verify(username, password)

    def ingroup(username, groupname)

When the default provider is used, the users' data exists within the `/_users/` node. The node contains a dictionary where keys are user names and values are objects containing information about the users, such as a hash. For instance, the user `hello` with a password `world` belonging to groups `administrators` and `data managers` will be stored this way:

    {
        "hello": {
            "hash": "$pbkdf2-sha256$100000$k1IqZUwphbA2RgghxPg/5w$iqYsBdtwBKxAI2p/HAOvFuKLfakQDhwFqzszP3IgD/w",
            "member-of": ["administrators", "data managers"]
        }
    }

The hash can be generated by `genpassword.py` in `extras` directory. The tool has three levels of security, set through `--level` option:

  - `poor`: the password is checked nearly instantly. This is suited for systems which are not intended to be particularly secure.

  - `normal`: the password takes some time to be checked, approximately 0.5 s. on a 2 GHz processor (the actual performance may vary *a lot*). This is suited for applications which handle non-sensitive data which should still be protected from public access.

  - `strong`: (default) the password takes a long time to be checked, approximately 1 s. on a 2 GHz processor (the actual performance may vary *a lot*). This is suited for applications which handle sensitive data such as root passwords of servers.

The longer is the check, the harder is for an attacker to crack the password if the attacker achieves to get the hashes.

The groups are stored in `/_groups/` node. The node contains a dictionary where keys are group names and values are objects containing information about the groups, such as the groups this group belongs to. Example:

    {
        "administrators": { },
        "data managers": {
            "member-of": ["backup operators"]
        },
        "backup operators": { },
    }

Let's use a few illustrations for which we use four users and four groups. Each user has the same password `demo`. Here's the actual contents of `/_users.json` file (hashes being trunkated for better readability):

    {
        "Lucy": {
            "hash": "$pbkdf2-sha256$10$7l0LYUxpzbn3H...",
            "member-of": ["users"]
        },
        "Emily": {
            "hash": "$pbkdf2-sha256$10$7l0LYUxpzbn3H...",
            "member-of": ["administrators"]
        },
        "William": {
            "hash": "$pbkdf2-sha256$10$7l0LYUxpzbn3H...",
            "member-of": ["backup operators"]
        },
        "James": {
            "hash": "$pbkdf2-sha256$10$7l0LYUxpzbn3H...",
            "member-of": ["users"]
        }
    }

Here are the groups. Notice the circular link between backup operators and administrators: Trust doesn't complain about it, so a user who belongs to backup operators group or the one who belongs to administrators group will belong to all three groups.

    {
        "users": { },
        "backup operators": {
            "member-of": ["users", "administrators"]
        },
        "administrators": {
            "member-of": ["backup operators"]
        }
    }

Credentials are checked only when private data is accessed. This is important, since the sole fact of providing credentials doesn't mean that they will be checked. In the following example, credentials are invalid, and still, no error is returned because credentials are not checked:

  - **illustration13/example.json**

        {
            "hello": 5
        }

  - **Result for `/illustration13/example/hello` using `--username William --password "invalid password"`**

        5

The checks are postponed for a reason. Checks are slow and have an important impact on the CPU, which means that in order to achieve better performance, the caller should know whether the accessed information is public or contains restricted nodes. However, callers may not necessarily know that information is restricted or public, and even if they know it, providing credentials in some cases but not in others can make the scripts unecessarily difficult.

Let's see how permissions work. We have a JSON file containing a node restricted to a specific user:

  - **illustration14/example.json**

        {
            "restricted": {
                ".special:restricted": {
                    "users": ["Lucy"]
                }
                "hello": "Hello, World"
            }
        }

We can get the piece of information when the correct credentials of this specific user are provided:

  - **Result for `/illustration14/restricted/hello` using `--response-mode json --username Lucy --password demo`**

        {
            "result": "Hello, World"
        }

On the other hand, a different user cannot access the data:

  - **Result for `/illustration14/restricted/hello` using `--response-mode json --username William --password demo`**

        {
            "errors": [
                {
                    "type": "permission-required",
                    "uri": "http://services.pelicandd.com/trust/error/permission-required",
                    "description": "A permission is required to be able to access the requested element."
                }
            ]
        }

The response is identical when a guest is trying to access the data:

  - **Result for `/illustration14/restricted/hello` using `--response-mode json --username William --password demo`**

        {
            "errors": [
                {
                    "type": "permission-required",
                    "uri": "http://services.pelicandd.com/trust/error/permission-required",
                    "description": "A permission is required to be able to access the requested element."
                }
            ]
        }

Groups work in the same way. Let's consider the following file:

  - **illustration15/example.json**

        {
            "restricted": {
                ".special:restricted": {
                    "groups": ["users"]
                },
                "hello": "Hello, World",
                "secrets": {
                    ".special:restricted": {
                        "groups": ["administrators"]
                    },
                    ".special:value": "Top secret"
                }
            }
        }

The whole contents of the file are restricted to "users" group, and `secrets` node is further restricted to administrators. For instance, James can access data, but not the secrets:

  - **Result for `/illustration15/restricted/hello` using `--username James --password demo`**

        "Hello, World"

  - **Result for `/illustration15/restricted/secrets` using `--response-mode json --username James --password demo`**

        {
            "errors": [
                {
                    "type": "permission-required",
                    "uri": "http://services.pelicandd.com/trust/error/permission-required",
                    "description": "A permission is required to be able to access the requested element."
                }
            ]
        }

Obviously, if we reverse the groups, James won't be access anything:

  - **illustration16/example.json**

        {
            "restricted": {
                ".special:restricted": {
                    "groups": ["administrators"]
                },
                "hello": "Hello, World",
                "secrets": {
                    ".special:restricted": {
                        "groups": ["users"]
                    },
                    ".special:value": "Top secret"
                }
            }
        }

  - **Result for `/illustration16/restricted/secrets` using `--response-mode json --username James --password demo`**

        {
            "errors": [
                {
                    "type": "permission-required",
                    "uri": "http://services.pelicandd.com/trust/error/permission-required",
                    "description": "A permission is required to be able to access the requested element."
                }
            ]
        }

Combining users and groups is possible too:

  - **illustration17/example.json**

        {
            "restricted": {
                ".special:restricted": {
                    "users": ["Lucy"],
                    "groups": ["administrators"]
                }
                "hello": "Hello, World"
            }
        }

Here, Lucy can access the node even if she is not part of administrators group:

  - **Result for `/illustration17/restricted/hello` using `--username Lucy --password demo`**

        "Hello, World"

Emily can access the node as well, since she is a member of administrators group:

  - **Result for `/illustration17/restricted/hello` using `--username Emily --password demo`**

        "Hello, World"

<h3 id="head-forbidden">Forbidden parts</h3>

For security reasons, some parts are forbidden in a query. Any access to `/_users` and `/_groups` nodes is forbidden. Another forbidden element are two dots surrounded by slashes (or a slash followed by two dots at the end of the query).

Data architects ye be warned: **accessing users and groups and using two dots is still possible through inheritance**.

Note that when Trust is accessed through a web service, URIs such as `http://example.com/a/../b` is automatically transformed by the client to `http://example.com/b`. This is why, for instance, CURL tests which use two dots won't generate a `query-invalid` error.

*Illustration 18: access of `_users` node*

  - **Result for `/_users` using `--response-mode json`**

        {
            "errors": [
                {
                    "type": "query-invalid",
                    "uri": "http://services.pelicandd.com/trust/error/query-invalid",
                    "description": "The query contains invalid characters or parts."
                }
            ]
        }

*Illustration 19: access inside `_users` node*

  - **Result for `/_users/Lucy` using `--response-mode json`**

        {
            "errors": [
                {
                    "type": "query-invalid",
                    "uri": "http://services.pelicandd.com/trust/error/query-invalid",
                    "description": "The query contains invalid characters or parts."
                }
            ]
        }

*Illustration 20: access to `_groups` node*

  - **Result for `/_groups` using `--response-mode json`**

        {
            "errors": [
                {
                    "type": "query-invalid",
                    "uri": "http://services.pelicandd.com/trust/error/query-invalid",
                    "description": "The query contains invalid characters or parts."
                }
            ]
        }

*Illustration 21: access inside `_groups` node*

  - **Result for `/_groups/administrators` using `--response-mode json`**

        {
            "errors": [
                {
                    "type": "query-invalid",
                    "uri": "http://services.pelicandd.com/trust/error/query-invalid",
                    "description": "The query contains invalid characters or parts."
                }
            ]
        }

<h3>Audit</h3>

The audit covers two scenarios:

 - Authentication. Both successful and failed authentication attempts are audited. Every record contains the user name.

 - Access to restricted nodes. When the node is accessed by an authorized user or when an unauthorized user or a guest attempts to access a restricted node, an audit record is created, specifying the user name, if any, and the accessed node.

Currently, the audit entries can be sent to syslog only. Later, it is expected to add support for Redis and MongoDB.

<h2 id="head-contribute">Contribute</h2>

If you have a technical question, you may post it on [Stack Overflow](http://stackoverflow.com/). You may also contact me by e-mail at [arseni.mourzenko@pelicandd.com](mailto:arseni.mourzenko@pelicandd.com)

The source code of the project is [hosted](http://source.pelicandd.com/infrastructure/trust/) in our own version control. If you want to contribute to the project, contact me so I give you access to the SVN servers.

Here are some technical details about the architecture.

When Trust receives a request, it selects a formatter based on the value of the response mode. This formatter is then in charge of the process. This may seem unnatural (why would a formatter be in charge, instead of being called only at the end of the process?), but this approach makes the code simpler. In fact, different formatters handle differently exceptions and warnings. For instance, some will catch exceptions while others will let them being thrown up the stack.

The formatter handles the request by using a finder. A finder corresponds more or less to what we call a data source in the documentation, given that some finders may correspond to multiple data sources.

Finders do all the major work: authentication, permissions and the actual loading of data.

That's all for now.
