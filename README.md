Pon3Ark
===============

A data extractor for the ark files from the mobile game "My Little Pony"

```
Required:
docopt==0.6.2
```

Dependencies can be installed with the following command:
```
> pip install -r requirements.txt
```

Extracting:
```
> python Pon3Ark.py -x <ark_file>
```
Creating:
```
> python Pon3Ark.py -c <ark_file> FILE...
```
Adding:
```
> python Pon3Ark.py -a <ark_file> FILE...
```
Listing:
```
> python Pon3Ark.py -t <ark_file>
```

Automated installation
==============

Linux
--------------

Ezpz.
```
> python3.4 setup.py install
```
Alternatively, you can specify the --user switch to install it locally, which doesn't require sudo privileges.

Project Current State
==============

* This project is currently under development.
* However, since the ark file format might change, it could stop working in the future.

Contribute
==============

* You wanna contribute ? Great.
* Fork and submit a pull request.

Legal informations
==============

(Copied from Evenprime's Luna's Dreamwalk project)

Please note that this software does NOT contain any copyrighted or trademarked
content of Gameloft, Hasbro or any other legal entity that may take offense
in the existence of this program, as far as I am aware of.

Further, it does not enable people to circumvent a *copy protection scheme*.
This application does not provide any means of copying or modifying the
original MLP application. And even if it would, providing software that does
help modify existing software is in and by itself not automatically a copyright
violation, and most often covered by the "reverse engineering" exception of the
DMCA

Therefore, in my humble opinion, the DMCA (and trademark related C&D letters)
should not be applicable to this software and I will likely take the necessary
legal steps (e.g. filing a DMCA counter-claim) in case it gets abused for
taking down this software.
