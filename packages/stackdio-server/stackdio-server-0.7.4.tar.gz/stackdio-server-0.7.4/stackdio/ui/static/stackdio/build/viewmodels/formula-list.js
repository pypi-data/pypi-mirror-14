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

define(["jquery","generics/pagination","models/formula"],function(e,t,n){"use strict";return t.extend({breadcrumbs:[{active:!0,title:"Formulas"}],model:n,baseUrl:"/formulas/",initialUrl:"/api/formulas/",sortableFields:[{name:"title",displayName:"Title",width:"25%"},{name:"uri",displayName:"Repo URL",width:"50%"},{name:"status",displayName:"Status",width:"10%"},{name:"privateGitRepo",displayName:"Private",width:"5%"}],openActionFormulaId:null,actionMap:{},reset:function(){this.openActionFormulaId=null,this.actionMap={},this._super()},processObject:function(e){this.actionMap.hasOwnProperty(e.id)&&e.availableActions(this.actionMap[e.id])},extraReloadSteps:function(){var t=e(".action-dropdown"),n=this;t.on("show.bs.dropdown",function(e){var t=parseInt(e.target.id);n.openActionFormulaId=t;var r=n.objects();for(var i=0,s=r.length;i<s;++i)if(r[i].id===t){r[i].loadAvailableActions();break}}),t.on("hide.bs.dropdown",function(){n.openActionFormulaId=null})}})});