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

define(["jquery","knockout","ladda","bootbox","select2"],function(e,t,s,a){"use strict";return function(){var o=this;o.breadcrumbs=[{active:!1,title:"Snapshots",href:"/snapshots/"},{active:!0,title:"New"}],o.accountSelector=e("#snapshotAccount"),o.accountSelector.select2({ajax:{url:"/api/cloud/accounts/",dataType:"json",delay:100,data:function(e){return{title:e.term}},processResults:function(e){return e.results.forEach(function(e){e.text=e.title}),e},cache:!0},theme:"bootstrap",placeholder:"Select an account...",templateResult:function(e){return e.loading?e.text:e.title+"  --  "+e.description},minimumInputLength:0}),o.accountSelector.on("select2:select",function(e){var t=e.params.data;o.accountId(t.id)}),o.accountId=t.observable(),o.title=t.observable(),o.description=t.observable(),o.snapshotId=t.observable(),o.sizeInGB=t.observable(),o.filesystemType=t.observable(),o.reset=function(){o.accountId(null),o.title(""),o.description(""),o.snapshotId(""),o.sizeInGB(0),o.filesystemType("")},o.removeErrors=function(t){t.forEach(function(t){var s=e("#"+t);s.removeClass("has-error");var a=s.find(".help-block");a.remove()})},o.createSnapshot=function(){var t=["account","title","description","snapshot_id","size_in_gb","filesystem_type"];o.removeErrors(t);var r=s.create(document.querySelector("#create-button"));r.start(),e.ajax({method:"POST",url:"/api/cloud/snapshots/",data:JSON.stringify({account:o.accountId(),title:o.title(),description:o.description(),snapshot_id:o.snapshotId(),size_in_gb:o.sizeInGB(),filesystem_type:o.filesystemType()})}).always(function(){r.stop()}).done(function(){window.location="/snapshots/"}).fail(function(s){var o="";try{var r=JSON.parse(s.responseText);for(var n in r)if(r.hasOwnProperty(n))if(t.indexOf(n)>=0){var i=e("#"+n);i.addClass("has-error"),r[n].forEach(function(e){i.append('<span class="help-block">'+e+"</span>")})}else if("non_field_errors"===n)r[n].forEach(function(t){if(t.indexOf("title")>=0){var s=e("#title");s.addClass("has-error"),s.append('<span class="help-block">A snapshot with this title already exists.</span>')}});else{var c=n.replace("_"," ");r[n].forEach(function(e){o+="<dt>"+c+"</dt><dd>"+e+"</dd>"})}o&&(o='<dl class="dl-horizontal">'+o+"</dl>")}catch(l){o="Oops... there was a server error.  This has been reported to your administrators."}o&&a.alert({title:"Error creating snapshot",message:o})})},o.reset()}});