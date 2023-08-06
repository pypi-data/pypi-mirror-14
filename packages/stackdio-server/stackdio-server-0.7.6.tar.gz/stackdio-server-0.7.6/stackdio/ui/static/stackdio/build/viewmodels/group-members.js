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

define(["jquery","knockout","bootbox","generics/pagination","models/user","models/group","select2"],function(e,r,t,s,o,u){"use strict";return s.extend({breadcrumbs:[{active:!1,title:"Groups",href:"/groups/"},{active:!1,title:window.stackdio.groupName,href:"/groups/"+window.stackdio.groupName+"/"},{active:!0,title:"Members"}],group:null,autoRefresh:!0,userSelector:e("#groupUser"),model:o,baseUrl:"/groups/",initialUrl:"/api/groups/"+window.stackdio.groupName+"/users/",sortableFields:[{name:"username",displayName:"Username",width:"90%"}],createSelector:function(){var e=this;this.userSelector.select2({ajax:{url:"/api/users/",dataType:"json",delay:100,data:function(e){return{username:e.term}},processResults:function(r){return r.results=r.results.filter(function(r){r.id=r.username,r.text=r.username;var t=!1;return e.objects().forEach(function(e){e.username()===r.username&&(t=!0)}),!t}),r},cache:!0},theme:"bootstrap",placeholder:"Add a user to this group...",minimumInputLength:0})},init:function(){this._super(),this.group=new u(window.stackdio.groupName,this),this.createSelector();var e=this;this.userSelector.on("select2:select",function(r){var t=r.params.data;e.group.addUser(t).done(function(){e.userSelector.empty(),e.userSelector.val(null).trigger("change"),e.userSelector.select2("open")})})},addUser:function(){}})});