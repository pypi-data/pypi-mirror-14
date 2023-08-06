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

define(["generics/labels","models/blueprint"],function(e,i){"use strict";return e.extend({breadcrumbs:[{active:!1,title:"Blueprints",href:"/blueprints/"},{active:!1,title:window.stackdio.blueprintTitle,href:"/blueprints/"+window.stackdio.blueprintId+"/"},{active:!0,title:"Labels"}],parentModel:i,parentId:window.stackdio.blueprintId,baseUrl:"/blueprints/",initialUrl:"/api/blueprints/"+window.stackdio.blueprintId+"/labels/"})});