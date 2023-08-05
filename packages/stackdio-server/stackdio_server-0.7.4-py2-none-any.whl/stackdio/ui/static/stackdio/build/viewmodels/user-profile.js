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

define(["jquery","knockout","models/user"],function(e,t,n){"use strict";return function(){var t=this;t.user=null,t.breadcrumbs=[{active:!0,title:"User Profile"}],t.subscription=null,t.reset=function(){t.subscription&&t.subscription.dispose(),t.user=new n(null,t);var r=e(".checkbox-custom");t.subscription=t.user.advanced.subscribe(function(e){e?r.checkbox("check"):r.checkbox("uncheck")}),t.user.waiting.done(function(){t.user.loadGroups()})},t.reset()}});