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

define(["jquery","knockout","models/stack","models/command"],function(t,s,a,i){"use strict";return function(){this.breadcrumbs=[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:"Stack Detail",href:"/stacks/"+window.stackdio.stackId+"/"},{active:!1,title:"Stack Commands",href:"/stacks/"+window.stackdio.stackId+"/commands/"},{active:!0,title:"Command Detail"}],this.stack=s.observable(null),this.command=s.observable(null),this.reset=function(){this.stack(new a(window.stackdio.stackId,this)),this.command(new i(window.stackdio.commandId,this))},this.runAgain=function(){this.stack().runCommand(this.command().hostTarget(),this.command().command()).done(function(){window.location="/stacks/"+window.stackdio.stackId+"/commands/"})},this.reset()}});