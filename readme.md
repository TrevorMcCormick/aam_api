# Adobe-AAM

#### Update 12.18.19 - v1.0 stable!

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
4. Install this repository via pip
    ```sh
    $ pip install git+git://github.com/trevormccormick/adobe-aam.git
    ```
5. Create a json file containing your AAM credentials
    ```py
    Client.from_json('aam_credentials.json')
    ```
### Current coverage includes:
* Traits
* TraitFolders
* Segments
* SegmentFolders
* Destinations
* DerivedSignals

#### [Examples are here!](https://github.com/TrevorMcCormick/adobe-aam/blob/master/examples.md)

###  Planned Features
* Custom reporting
* d3 dashboard
