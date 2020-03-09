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
| Traits | Update Many Traits | ```Traits.update(file_path)```|
| TraitFolders | Get All Trait Folders | ```TraitFolders.get_many()```|
| TraitFolders | Get One Trait Folders | ```TraitFolders.get_one(folderId)```|
| TraitFolders | Search Trait Folders by Keyword | ```TraitFolders.search(column="name", type="all", keywords=["term1", "term2"])```|
| Segments | Get All Segments | ```Segments.get_many()```|
| Segments | Get One Segments | ```Segments.get_one(sid)```|
| Segments | Search Segments by Keyword | ```Segments.search("all", ["term1", "term2"])```|
| Segments | Get Segment Limits | ```Segments.get_limits()```|
| Segments | Get Segment Mappings | ```Segments.get_one_destinations(sid)```|
| Segments | Create Many Segments | ```Segments.create()```|
| Segments | Delete Many Segments | ```Segments.delete()```|
| Segments | Update Many Segments | ```Segments.update(file_path)```|
| SegmentFolders | Get All Segment Folders | ```SegmentFolders.get_many()```|
| SegmentFolders | Get One Segment Folders | ```SegmentFolders.get_one(folderId)```|
| SegmentFolders | Search Segment Folders by Keyword | ```SegmentFolders.search("all", ["term1", "term2"])```|
| Destinations | Get All Destinations | ```Destinations.get_many()```|
| Destinations | Get One Destination | ```Destination.get_one(destinationId)```|
| Destinations | Create Many Destinations | ```Destinations.create()```|
| Derived Signals | Get All Derived Signals | ```DerivedSignals.get_many()```|
| Derived Signals | Create Many Derived Signals | ```DerivedSignals.create()```|  
| Users | Get All Users | ```Users.get_many()```|  
| Reports | Get Traits Trend Report | ```Reports.traits_trend(traitId, "2020-03-01", "2020-03-08")


#### Specific Examples
Overall Trait Create Count by User
```
traits = Traits.get_many(includeUsers=True)
traits.groupby(['create_email']).count()['sid'].sort_values(ascending=False)
```

Traits that are over a month old and have not registered any Lifetime Trait Realizations
```
traits[(traits['createTime'] < thirty_days_ago) & (traits['uniquesLifetime'] == 0)]
```

Get list of possible arguments and descriptions for arguments of a function
```
help(Traits.get_many)
```
