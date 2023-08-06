/*!
  * Copyright 2016,  Digital Reasoning
  *
  * Licensed under the Apache License, Version 2.0 (the "License");
  * you may not use this file except in compliance with the License.
  * You may obtain a copy of the License at
  *
  *     http://www.apache.org/licenses/LICENSE-2.0
  *
  * Unless required by applicable law or agreed to in writing, software
  * distributed under the License is distributed on an "AS IS" BASIS,
  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  * See the License for the specific language governing permissions and
  * limitations under the License.
  *
*/

define(["jquery","generics/pagination","models/snapshot"],function(e,i,s){"use strict";return i.extend({breadcrumbs:[{active:!0,title:"Snapshots"}],model:s,baseUrl:"/snapshots/",initialUrl:"/api/cloud/snapshots/",detailRequiresAdvanced:!0,sortableFields:[{name:"title",displayName:"Title",width:"20%"},{name:"description",displayName:"Description",width:"20%"},{name:"snapshotId",displayName:"ID",width:"20%"},{name:"sizeInGB",displayName:"Size",width:"15%"},{name:"filesystemType",displayName:"Filesystem Type",width:"15%"}]})});