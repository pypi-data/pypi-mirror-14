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

define(["jquery","generics/pagination","models/stack"],function(e,t,n){"use strict";return t.extend({breadcrumbs:[{active:!0,title:"Stacks"}],model:n,baseUrl:"/stacks/",initialUrl:"/api/stacks/",sortableFields:[{name:"title",displayName:"Title",width:"15%"},{name:"description",displayName:"Description",width:"20%"},{name:"namespace",displayName:"Namespace",width:"15%"},{name:"created",displayName:"Launched",width:"15%"},{name:"hostCount",displayName:"Hosts",width:"10%"},{name:"status",displayName:"Status",width:"10%"}],openActionStackId:null,actionMap:{},reset:function(){this.openActionStackId=null,this.actionMap={},this._super()},processObject:function(e){this.actionMap.hasOwnProperty(e.id)&&e.availableActions(this.actionMap[e.id])},extraReloadSteps:function(){var t=e(".action-dropdown"),n=this;t.on("show.bs.dropdown",function(e){var t=parseInt(e.target.id);n.openActionStackId=t;var r=n.objects();for(var i=0,s=r.length;i<s;++i)if(r[i].id===t){r[i].loadAvailableActions();break}}),t.on("hide.bs.dropdown",function(){n.openActionStackId=null})}})});