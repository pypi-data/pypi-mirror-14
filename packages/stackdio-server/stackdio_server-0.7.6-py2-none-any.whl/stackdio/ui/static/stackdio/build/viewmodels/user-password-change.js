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

define(["jquery","knockout","bootbox"],function(r,e,s){"use strict";return function(){var a=this;a.breadcrumbs=[{active:!1,title:"Profile",href:"/user/"},{active:!0,title:"Change Password"}],a.currentPassword=e.observable(),a.newPassword1=e.observable(),a.newPassword2=e.observable(),a.reset=function(){a.currentPassword(""),a.newPassword1(""),a.newPassword2("")},a.removeErrors=function(e){e.forEach(function(e){var s=r("#"+e);s.removeClass("has-error");var a=s.find(".help-block");a.remove()})},a.changePassword=function(){var e=["current_password","new_password1","new_password2"];a.removeErrors(e),r.ajax({method:"POST",url:"/api/user/password/",data:JSON.stringify({current_password:a.currentPassword(),new_password1:a.newPassword1(),new_password2:a.newPassword2()})}).done(function(){window.location="/user/"}).fail(function(a){var o="";try{var n=JSON.parse(a.responseText);for(var t in n)if(n.hasOwnProperty(t))if(e.indexOf(t)>=0){var d=r("#"+t);d.addClass("has-error"),n[t].forEach(function(r){d.append('<span class="help-block">'+r+"</span>")})}else{var i=t.replace("_"," ");n[t].forEach(function(r){o+="<dt>"+i+"</dt><dd>"+r+"</dd>"})}o&&(o='<dl class="dl-horizontal">'+o+"</dl>")}catch(c){o="Oops... there was a server error.  This has been reported to your administrators."}o&&s.alert({title:"Error changing password",message:o})})},a.reset()}});