# AAM_API

#### Updated 02.20.2020 - stable

This is a Python wrapper for the Adobe Audience Manager API.

To get started:
1. Request a non-Marketing Cloud user account from your Adobe consultant
2. Obtain your enterprise Client ID and Client Secret from your Adobe consultant
3. Create a json file containing your AAM credentials:  
    **clientID**: "clientID",  

    **clientSecret**:"clientSecret",  

    **partnerName**:"partnerName",  

    **username**:"username",  

    **password**:"password",
4. Install this repository via PyPi
    ```sh
    $ pip install aam_api
    ```
5. Import aam_api and provide path to credentials file.
    ```py
    from aam_api import *
    ```
    Provide the path to your AAM credentials file.
    Note-- if you save your file as "aam_credentials.json" in the folder you launched Python, you can skip this step.

#### [Examples are here!](https://github.com/TrevorMcCormick/aam_api/blob/master/examples.md)

### Current coverage [Create, Read, Update, Delete] includes:
* Traits [CRUD]
* TraitFolders [R]
* Segments [CRUD]
* SegmentFolders [R]
* Destinations [CRD]
* DerivedSignals [CR]
* Users [R]
* Reports (Traits Trend) [R]

### Current extra features [Read] include:
* Mapper
- Segments mapped to Destination ID
- Traits mapped to Segment ID
- Traits mapped to other Trait IDs

###  Planned Features
* Custom reporting and data extract templates
