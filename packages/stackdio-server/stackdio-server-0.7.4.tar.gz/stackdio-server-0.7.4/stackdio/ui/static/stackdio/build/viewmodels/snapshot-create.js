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

define(["jquery","knockout","ladda","bootbox","select2"],function(e,t,n,r){"use strict";return function(){var i=this;i.breadcrumbs=[{active:!1,title:"Snapshots",href:"/snapshots/"},{active:!0,title:"New"}],i.accountSelector=e("#snapshotAccount"),i.accountSelector.select2({ajax:{url:"/api/cloud/accounts/",dataType:"json",delay:100,data:function(e){return{title:e.term}},processResults:function(e){return e.results.forEach(function(e){e.text=e.title}),e},cache:!0},theme:"bootstrap",placeholder:"Select an account...",templateResult:function(e){return e.loading?e.text:e.title+"  --  "+e.description},minimumInputLength:0}),i.accountSelector.on("select2:select",function(e){var t=e.params.data;i.accountId(t.id)}),i.accountId=t.observable(),i.title=t.observable(),i.description=t.observable(),i.snapshotId=t.observable(),i.sizeInGB=t.observable(),i.filesystemType=t.observable(),i.reset=function(){i.accountId(null),i.title(""),i.description(""),i.snapshotId(""),i.sizeInGB(0),i.filesystemType("")},i.removeErrors=function(t){t.forEach(function(t){var n=e("#"+t);n.removeClass("has-error");var r=n.find(".help-block");r.remove()})},i.createSnapshot=function(){var t=["account","title","description","snapshot_id","size_in_gb","filesystem_type"];i.removeErrors(t);var s=n.create(document.querySelector("#create-button"));s.start(),e.ajax({method:"POST",url:"/api/cloud/snapshots/",data:JSON.stringify({account:i.accountId(),title:i.title(),description:i.description(),snapshot_id:i.snapshotId(),size_in_gb:i.sizeInGB(),filesystem_type:i.filesystemType()})}).always(function(){s.stop()}).done(function(){window.location="/snapshots/"}).fail(function(n){var i="";try{var s=JSON.parse(n.responseText);for(var o in s)if(s.hasOwnProperty(o))if(t.indexOf(o)>=0){var u=e("#"+o);u.addClass("has-error"),s[o].forEach(function(e){u.append('<span class="help-block">'+e+"</span>")})}else if(o==="non_field_errors")s[o].forEach(function(t){if(t.indexOf("title")>=0){var n=e("#title");n.addClass("has-error"),n.append('<span class="help-block">A snapshot with this title already exists.</span>')}});else{var a=o.replace("_"," ");s[o].forEach(function(e){i+="<dt>"+a+"</dt><dd>"+e+"</dd>"})}i&&(i='<dl class="dl-horizontal">'+i+"</dl>")}catch(f){i="Oops... there was a server error.  This has been reported to your administrators."}i&&r.alert({title:"Error creating snapshot",message:i})})},i.reset()}});