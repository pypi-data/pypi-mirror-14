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

define(["jquery","generics/pagination","models/formula"],function(i,t,a){"use strict";return t.extend({breadcrumbs:[{active:!0,title:"Formulas"}],model:a,baseUrl:"/formulas/",initialUrl:"/api/formulas/",sortableFields:[{name:"title",displayName:"Title",width:"25%"},{name:"uri",displayName:"Repo URL",width:"50%"},{name:"status",displayName:"Status",width:"10%"},{name:"privateGitRepo",displayName:"Private",width:"5%"}],openActionFormulaId:null,actionMap:{},reset:function(){this.openActionFormulaId=null,this.actionMap={},this._super()},processObject:function(i){this.actionMap.hasOwnProperty(i.id)&&i.availableActions(this.actionMap[i.id])},extraReloadSteps:function(){var t=i(".action-dropdown"),a=this;t.on("show.bs.dropdown",function(i){var t=parseInt(i.target.id);a.openActionFormulaId=t;for(var e=a.objects(),o=0,n=e.length;n>o;++o)if(e[o].id===t){e[o].loadAvailableActions();break}}),t.on("hide.bs.dropdown",function(){a.openActionFormulaId=null})}})});