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

define(["jquery","knockout","generics/pagination","models/formula","models/component","select2"],function(e,t,n,r,i){"use strict";return n.extend({breadcrumbs:[{active:!1,title:"Formulas",href:"/formulas/"},{active:!0,title:window.stackdio.formulaTitle}],model:i,baseUrl:"/formulas/"+window.stackdio.formulaId+"/",initialUrl:"/api/formulas/"+window.stackdio.formulaId+"/components/",sortableFields:[{name:"title",displayName:"Title",width:"30%"},{name:"description",displayName:"Description",width:"50%"},{name:"slsPath",displayName:"SLS Path",width:"20%"}],autoRefresh:!1,formula:null,formulaUrl:t.observable(""),init:function(){function i(){n.formula.reload(),n.formula.loadComponents()}this._super();var n=this;this.formula=new r(window.stackdio.formulaId,this),this.formula.waiting.done(function(){document.title="stackd.io | Formula Detail - "+n.formula.title()}).fail(function(){window.location="/formulas/"}),this.usernameText=t.computed(function(){return n.formula.accessToken()?"GitHub access token":"Git username"}),this.versionSelector=e("#formulaVersion"),this.versionSelector.select2({ajax:{url:this.formula.raw.valid_versions,dataType:"json",delay:100,data:function(e){return{version:e.term}},processResults:function(e){var t=[];return e.results.forEach(function(e){t.push({id:e,version:e,text:e})}),{count:e.count,results:t}},cache:!0},theme:"bootstrap",placeholder:"Select a version...",minimumInputLength:0}),this.versionSelector.on("select2:select",function(e){var t=e.params.data;n.currentPage(n.initialUrl+"?version="+t.version),n.shouldReset=!1,n.reset()}),e(".action-dropdown").on("show.bs.dropdown",function(){n.formula.loadAvailableActions()}),setInterval(i,3e3)}})});