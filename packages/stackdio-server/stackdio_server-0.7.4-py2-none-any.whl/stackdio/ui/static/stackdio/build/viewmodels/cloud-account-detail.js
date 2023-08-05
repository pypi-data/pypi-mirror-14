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

define(["jquery","knockout","models/cloud-account"],function(e,t,n){"use strict";return function(){var r=this;r.account=null,r.accountUrl=t.observable(""),r.breadcrumbs=[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!0,title:window.stackdio.accountTitle}],r.subscription=null,r.reset=function(){r.subscription&&r.subscription.dispose(),r.account=new n(window.stackdio.accountId,r),r.account.waiting.done(function(){document.title="stackd.io | Cloud Account Detail - "+r.account.title()}).fail(function(){window.location="/accounts/"});var t=e(".checkbox-custom");r.subscription=r.account.createSecurityGroups.subscribe(function(e){e?t.checkbox("check"):t.checkbox("uncheck")})},r.reset()}});