/*!
  * Copyright 2014,  Digital Reasoning
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

define(["jquery","knockout","models/snapshot"],function(e,t,n){"use strict";return function(){var e=this;e.snapshot=null,e.snapshotUrl=t.observable(""),e.breadcrumbs=[{active:!1,title:"Snapshots",href:"/snapshots/"},{active:!0,title:window.stackdio.snapshotTitle}],e.reset=function(){e.snapshot=new n(window.stackdio.snapshotId,e),e.snapshot.waiting.done(function(){document.title="stackd.io | Snapshot Detail - "+e.snapshot.title()}).fail(function(){window.location="/snapshots/"})},e.reset()}});