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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/command"],function(t,a,s,i,n,e){"use strict";return i.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Commands"}],stack:a.observable(),autoRefresh:!0,model:e,baseUrl:"/stacks/"+window.stackdio.stackId+"/commands/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/commands/",sortableFields:[{name:"hostTarget",displayName:"Host Target",width:"15%"},{name:"command",displayName:"Command",width:"40%"},{name:"finishTime",displayName:"Finished",width:"25%"},{name:"status",displayName:"Status",width:"10%"}],hostTarget:a.observable(null),command:a.observable(null),init:function(){this._super(),this.stack(new n(window.stackdio.stackId,this))},runCommand:function(){var t=this;this.stack().runCommand(this.hostTarget(),this.command()).done(function(){t.hostTarget(""),t.command("")})},runAgain:function(t){var a=this;this.stack().runCommand(t.hostTarget(),t.command()).done(function(){a.hostTarget(""),a.command("")})}})});