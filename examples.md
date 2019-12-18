# Adobe-AAM

#### Examples
These are basic examples. Peek into the repo to see the available parameters.  


| API Endpoint |   Action   |   Code   |
|:---------|------------|:---------|
| Oauth | Log In |```Client.from_json(file_path) ``` |
| Traits | Get All Traits | ```Traits.get_many()```|
| Traits | Get One Trait | ```Traits.get_one(traitId)```|
| Traits | Search Traits by Keyword | ```Traits.search(column="name", type="all", keywords=["term1", "term2"])```|
| Traits | Get Trait Limits | ```Traits.get_limits()```|
| Traits | Create Many Traits | ```Traits.create(file_path)```|
| Traits | Delete Many Traits | ```Traits.delete(file_path)```|
| TraitFolders | Get All Trait Folders | ```TraitFolders.get_many()```|
| TraitFolders | Get One Trait Folders | ```TraitFolders.get_one(folderId)```|
| TraitFolders | Search Trait Folders by Keyword | ```TraitFolders.search(column="name", type="all", keywords=["term1", "term2"])```|
| Segments | Get All Segments | ```Segments.get_many()```|
| Segments | Get One Segments | ```Segments.get_one(sid)```|
| Segments | Search Segments by Keyword | ```Segments.search("all", ["term1", "term2"])```|
| Segments | Get Segment Limits | ```Segments.get_limits()```|
| Segments | Get Segment Mappings | ```Segments.get_one_destinations(sid)```|
| Segments | Create Many Segments | ~~```Segments.create()```~~|
| Segments | Delete Many Segments | ```Segments.delete()```|
| SegmentFolders | Get All Segment Folders | ```SegmentFolders.get_many()```|
| SegmentFolders | Get One Segment Folders | ```SegmentFolders.get_one(folderId)```|
| SegmentFolders | Search Segment Folders by Keyword | ```SegmentFolders.search("all", ["term1", "term2"])```|
| Destinations | Get All Destinations | ```Destinations.get_many()```|
| Destinations | Get One Destination | ```Destination.get_one(destinationId)```|
| Destinations | Create Many Destinations | ```Destinations.create()```|
| Derived Signals | Get All Derived Signals | ```DerivedSignals.get_many()```|
| Destinations | Create Many Destinations | ```Destinations.create()```|
