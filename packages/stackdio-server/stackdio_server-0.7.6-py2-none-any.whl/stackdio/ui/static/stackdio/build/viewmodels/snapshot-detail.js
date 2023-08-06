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

define(["jquery","knockout","models/snapshot"],function(t,s,n){"use strict";return function(){var t=this;t.snapshot=null,t.snapshotUrl=s.observable(""),t.breadcrumbs=[{active:!1,title:"Snapshots",href:"/snapshots/"},{active:!0,title:window.stackdio.snapshotTitle}],t.reset=function(){t.snapshot=new n(window.stackdio.snapshotId,t),t.snapshot.waiting.done(function(){document.title="stackd.io | Snapshot Detail - "+t.snapshot.title()}).fail(function(){window.location="/snapshots/"})},t.reset()}});