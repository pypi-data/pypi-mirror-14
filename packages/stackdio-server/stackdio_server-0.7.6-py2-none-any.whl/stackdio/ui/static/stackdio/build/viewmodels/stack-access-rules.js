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

define(["jquery","knockout","bootbox","generics/pagination","models/stack","models/security-group"],function(t,s,a,e,i,n){"use strict";return e.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Access Rules"}],stack:s.observable(),autoRefresh:!0,model:n,baseUrl:"/stacks/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/security_groups/",sortableFields:[{name:"name",displayName:"Name",width:"40%"},{name:"description",displayName:"Description",width:"40%"},{name:"groupId",displayName:"Group ID",width:"20%"}],hostTarget:s.observable(null),command:s.observable(null),init:function(){this._super(),this.stack(new i(window.stackdio.stackId,this))},runCommand:function(){var t=this;this.stack().runCommand(this.hostTarget(),this.command()).done(function(){t.hostTarget(""),t.command("")})},runAgain:function(t){var s=this;this.stack().runCommand(t.hostTarget(),t.command()).done(function(){s.hostTarget(""),s.command("")})}})});