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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/command"],function(e,t,n,r,i,s){"use strict";return r.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Commands"}],stack:t.observable(),autoRefresh:!0,model:s,baseUrl:"/stacks/"+window.stackdio.stackId+"/commands/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/commands/",sortableFields:[{name:"hostTarget",displayName:"Host Target",width:"15%"},{name:"command",displayName:"Command",width:"40%"},{name:"finishTime",displayName:"Finished",width:"25%"},{name:"status",displayName:"Status",width:"10%"}],hostTarget:t.observable(null),command:t.observable(null),init:function(){this._super(),this.stack(new i(window.stackdio.stackId,this))},runCommand:function(){var e=this;this.stack().runCommand(this.hostTarget(),this.command()).done(function(){e.hostTarget(""),e.command("")})},runAgain:function(e){var t=this;this.stack().runCommand(e.hostTarget(),e.command()).done(function(){t.hostTarget(""),t.command("")})}})});