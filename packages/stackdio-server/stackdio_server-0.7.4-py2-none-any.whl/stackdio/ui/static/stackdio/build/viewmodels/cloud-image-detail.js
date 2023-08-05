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

define(["jquery","knockout","models/cloud-image","models/cloud-account","select2"],function(e,t,n,r){"use strict";return function(){var i=this;i.image=null,i.account=null,i.imageUrl=t.observable(""),i.accountTitle=t.observable(),i.accountUrl="/accounts/"+window.stackdio.accountId+"/",i.accountId=t.observable(""),document.referrer.indexOf("account")>=0?i.breadcrumbs=[{active:!1,title:"Cloud Accounts",href:"/accounts/"},{active:!1,title:window.stackdio.accountTitle,href:t.computed(function(){return"/accounts/"+i.accountId()+"/"})},{active:!1,title:"Images",href:t.computed(function(){return"/accounts/"+i.accountId()+"/images/"})},{active:!0,title:window.stackdio.imageTitle}]:i.breadcrumbs=[{active:!1,title:"Cloud Images",href:"/images/"},{active:!0,title:window.stackdio.imageTitle}],i.sizeSelector=e("#imageDefaultInstanceSize"),i.sizeSelector.select2({ajax:{url:"/api/cloud/providers/"+window.stackdio.providerName+"/instance_sizes/",dataType:"json",delay:100,data:function(e){return{instance_id:e.term}},processResults:function(e){return e.results.forEach(function(e){e.id=e.instance_id,e.text=e.instance_id}),e},cache:!0},theme:"bootstrap",placeholder:"Select an instance size...",minimumInputLength:0}),i.sizeSelector.on("select2:select",function(e){var t=e.params.data;i.image.defaultInstanceSize(t.instance_id)}),i.reset=function(){i.image=new n(window.stackdio.imageId,i),i.account=new r(window.stackdio.accountId,i),i.image.waiting.done(function(){document.title="stackd.io | Cloud Image Detail - "+i.image.title(),i.accountId(i.image.raw.account);var e=i.image.defaultInstanceSize();i.sizeSelector.append('<option value="'+e+'" title="'+e+'">'+e+"</option>"),i.sizeSelector.val(e).trigger("change")}).fail(function(){window.location="/images/"}),i.account.waiting.done(function(){i.accountTitle(i.account.title()+"  --  "+i.account.description())})},i.reset()}});