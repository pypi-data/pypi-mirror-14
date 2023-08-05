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

define(["jquery","knockout","models/stack"],function(e,t,n){"use strict";return function(){var r=this;r.stack=null,r.blueprintTitle=t.observable(window.stackdio.blueprintTitle),r.blueprintUrl=t.observable("/blueprints/"+window.stackdio.blueprintId+"/"),r.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!0,title:window.stackdio.stackTitle}],r.subscription=null,r.reset=function(){r.subscription&&r.subscription.dispose(),r.stack=new n(window.stackdio.stackId,r),r.stack.waiting.done(function(){document.title="stackd.io | Stack Detail - "+r.stack.title()}).fail(function(){window.location="/stacks/"});var t=e(".checkbox-custom");r.subscription=r.stack.createUsers.subscribe(function(e){e?t.checkbox("check"):t.checkbox("uncheck")})},r.refreshStack=function(){r.stack.refreshStatus().fail(function(){window.location="/stacks/"}),r.stack.loadHistory()},e(".action-dropdown").on("show.bs.dropdown",function(){r.stack.loadAvailableActions()}),r.reset(),r.refreshStack(),setInterval(r.refreshStack,3e3)}});