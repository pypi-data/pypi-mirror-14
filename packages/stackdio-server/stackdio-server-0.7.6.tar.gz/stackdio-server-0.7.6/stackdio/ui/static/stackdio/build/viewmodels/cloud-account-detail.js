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

define(["jquery","knockout","models/cloud-account"],function(c,t,o){"use strict";return function(){var n=this;n.account=null,n.accountUrl=t.observable(""),n.breadcrumbs=[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!0,title:window.stackdio.accountTitle}],n.subscription=null,n.reset=function(){n.subscription&&n.subscription.dispose(),n.account=new o(window.stackdio.accountId,n),n.account.waiting.done(function(){document.title="stackd.io | Cloud Account Detail - "+n.account.title()}).fail(function(){window.location="/accounts/"});var t=c(".checkbox-custom");n.subscription=n.account.createSecurityGroups.subscribe(function(c){c?t.checkbox("check"):t.checkbox("uncheck")})},n.reset()}});