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

define(["jquery","knockout","models/cloud-image","models/cloud-account","select2"],function(e,t,c,i){"use strict";return function(){var a=this;a.image=null,a.account=null,a.imageUrl=t.observable(""),a.accountTitle=t.observable(),a.accountUrl="/accounts/"+window.stackdio.accountId+"/",a.accountId=t.observable(""),document.referrer.indexOf("account")>=0?a.breadcrumbs=[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!1,title:window.stackdio.accountTitle,href:t.computed(function(){return"/accounts/"+a.accountId()+"/"})},{active:!1,title:"Images",href:t.computed(function(){return"/accounts/"+a.accountId()+"/images/"})},{active:!0,title:window.stackdio.imageTitle}]:a.breadcrumbs=[{active:!1,title:"Cloud Images",href:"/images/"},{active:!0,title:window.stackdio.imageTitle}],a.sizeSelector=e("#imageDefaultInstanceSize"),a.sizeSelector.select2({ajax:{url:"/api/cloud/providers/"+window.stackdio.providerName+"/instance_sizes/",dataType:"json",delay:100,data:function(e){return{instance_id:e.term}},processResults:function(e){return e.results.forEach(function(e){e.id=e.instance_id,e.text=e.instance_id}),e},cache:!0},theme:"bootstrap",placeholder:"Select an instance size...",minimumInputLength:0}),a.sizeSelector.on("select2:select",function(e){var t=e.params.data;a.image.defaultInstanceSize(t.instance_id)}),a.reset=function(){a.image=new c(window.stackdio.imageId,a),a.account=new i(window.stackdio.accountId,a),a.image.waiting.done(function(){document.title="stackd.io | Cloud Image Detail - "+a.image.title(),a.accountId(a.image.raw.account);var e=a.image.defaultInstanceSize();a.sizeSelector.append('<option value="'+e+'" title="'+e+'">'+e+"</option>"),a.sizeSelector.val(e).trigger("change")}).fail(function(){window.location="/images/"}),a.account.waiting.done(function(){a.accountTitle(a.account.title()+"  --  "+a.account.description())})},a.reset()}});