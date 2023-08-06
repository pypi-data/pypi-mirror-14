ocapi
=====

This is API connector to http://www.pripravto.cz service for furniture makers. You should
be able to use it to create your custom designs for furniture, download data
and eventually build your partial interface. Connector is built on HTTP GET and
POST methods and it uses your account on service.

For this project we are using PyVmMonitor on http://www.pyvmmonitor.com

Instalation
-----------

For instalation you can download package or install by **pip**. Downloaded you
can just unpack or get from from https://pypi.python.org/pypi/ocapi and install it::

    #download archive
    wget https://bitbucket.org/pripravto/ocapi/get/default.tar.gz
    cd /tmp
    virtualenv test
    source test/bin/activate
    tar -xvf default.tar.gz
    #specify correct name
    cd pripravto....

Instalation::

    python setup.py install

or install by pip::

    pip install ocapi


Quickstart
----------

First you should get your account on **https://pripravto.cz** service, when you will have it
Login normally into service. Then you can start by opening Python console
and importing ocapi::

    import ocapi.api as oc
    import math
    args = {'name':'test2','position':[0,0,0],'size':[1000,1000,1000]}
    #set your user credentials here
    prod = oc.CabinetMaker(args, username="test",password="test")
    for i in range(36):
        size = [18,math.sin(math.radians(i*10))*50+80,18]
        rot = [0,0,10+i*2]
        prod.add_element(pos=[i*20,0,0],size=size,rot=rot)
    prod.finish()

This is partial example which will show you base usage of this api. This will create
serries of elements which are sized by sin function and rotated by series of
iteration.

To build something more usefull you can make first base cabinet by just writing down
one function::

    args = {'name':'cabinet2','position':[0,0,0],'size':[600,600,1000]}
    prod.parse_args(args)
    #build our base parts
    prod.add_basic()
    #add doors
    prod.add_doors()
    prod.finish()

After data creation you can also check what kind of data you have created on service
itself and also download images and so on.

Username and password are specified at start of object::

    prod = oc.CabinetMaker(args, username="test",password="test", host="test.pripravto.cz")
    #your username and password is from https://pripravto.cz/oc/oc/register/start

For complete registration process you need your functional e-mail address and fill out
data required by registration. **You should keep your user credentials secret.**
For examples what can be built on this api connector take a look on http://pripravto.cz/en/blog
where we put examples.

More comples example can be::


    args = {'size': [1200, 600, 900], 'thickConstr': 18, 'frontOut': True, 'socle': 0, 'doorShift': 0, 'matConstr': '45', 'elementInfo': {'fittings': {'KOL': 5}, 'production': {'EDGEBANDER': 2, 'HAND': 3, 'SAW': 1, 'CNC': 1, 'COATING': False}, 'group': 'spodni_2', 'visibility': 'NORMAL', 'block': True}, 'position': [2700, 0, 0], 'rotation': [-30, 0, 0], 'matFront': 'U625', 'name': 'spodni_2'}
    spodni_2 = oc.CabinetMaker(args, username="test",password="test")
    spodni_2.add_top(info=None,area_id=None,mat='F870',bars_width=None,pos=None,diff=None,save=True,size=38)
    spodni_2.add_frame(info=None,area_id=None,thick_fill=None,mat=45,diff_fill=[0, 0, 5, 0, 0, 0],insert_fill=False,width=150,mat_fill=None,low_profile=False,planes=4,diff=[0, 50, 50, 0, 0, 0],thick=18,save=True,order=[0, 2, 1])
    spodni_2.add_dividers(info=None,area_id=None,array_dist=[2, 1],mat=None,part_size=None,thickness=None,part=False,diff=None,save=True,typ='B',areas=True)
    spodni_2.add_basic(info=None,area_id=True,variant='H',back=5,socle=None,diff=None,save=True,top_bars=None)
    spodni_2.add_shelve(info=None,area_id=True,mat=None,number=[4, 4, 5],diff=None,rotation=None,save=True,size=None)
    spodni_2.add_doors(info=None,area_id=0,handleHeight='TOP',mat=None,grains=True,handleSize=[160, 25, 5],stacking='HORIZONTAL',number=2,door_type='AUTOMAT',handleSide=None,diff=None,handleOrientation='VERTICAL',pars_front=[3, 3, 3, 3, 3],save=True,handlePos=[50, 50])
    spodni_2.add_doors(info=None,area_id=1,handleHeight='TOP',mat=None,grains=True,handleSize=[160, 25, 5],stacking='HORIZONTAL',number=1,door_type='AUTOMAT',handleSide=None,diff=None,handleOrientation='VERTICAL',pars_front=[3, 3, 3, 3, 3],save=True,handlePos=[50, 50])
    spodni_2.finish()
    spodni_2.get_image()

This example creates base part for kitchen and it has several other items, which
are generated on the fly by oc service.

If you want to set your **crendentials** to be all the time in your way,
just make subclass to **CabinetMaker** and set your default parameters in init.


More documantation for pripravto service or about this plase see web page or
**oc.CabinetMaker** class.

Other data
----------

It should be also possible to download other images like optimalization and
vizualization from server. Possible solution is to use it like this.

    con.

Development
-----------

You can contact us or raise issues on https://bitbucket.org/pripravto/ocapi
Developmnet is also made on Bitbucket, you can clone repository and start
making chaneges. We also plan to use this api connector to be able to connect
with diffrent applications more quickly and easily.

