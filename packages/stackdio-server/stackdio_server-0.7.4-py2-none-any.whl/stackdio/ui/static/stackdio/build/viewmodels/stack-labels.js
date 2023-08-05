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

define(["jquery","knockout","bootbox","utils/utils","generics/pagination","models/stack","models/label"],function(e,t,n,r,i,s,o){"use strict";return i.extend({breadcrumbs:[{active:!1,title:"Stacks",href:"/stacks/"},{active:!1,title:window.stackdio.stackTitle,href:"/stacks/"+window.stackdio.stackId+"/"},{active:!0,title:"Labels"}],stack:t.observable(),newLabels:t.observableArray([]),newLabelKey:t.observable(),autoRefresh:!1,model:o,baseUrl:"/stacks/",initialUrl:"/api/stacks/"+window.stackdio.stackId+"/labels/",sortableFields:[{name:"key",displayName:"Key",width:"45%"},{name:"value",displayName:"Value",width:"45%"}],init:function(){this._super(),this.newLabelKey(null),this.stack(new s(window.stackdio.stackId,this))},addNewLabel:function(){var n=e("#new-label-form");n.removeClass("has-error");var i=this,s=!1;this.sortedObjects().forEach(function(e){e.key()===i.newLabelKey()&&(s=!0)}),this.newLabels().forEach(function(e){e.key===i.newLabelKey()&&(s=!0)});if(s){r.growlAlert("You may not have two labels with the same key.","danger"),n.addClass("has-error");return}this.newLabels.push({key:this.newLabelKey(),value:t.observable(null)}),this.newLabelKey(null)},deleteNewLabel:function(e){this.newLabels.remove(e)},saveLabels:function(){var t=[],n=this;this.objects().forEach(function(i){t.push(e.ajax({method:"PUT",url:n.stack().raw.labels+i.key()+"/",data:JSON.stringify({value:i.value()})}).fail(function(e){e.status!==404&&r.alertError(e,"Error saving label","Errors saving label for "+i.key()+":<br>")}))}),this.newLabels().forEach(function(i){t.push(e.ajax({method:"POST",url:n.stack().raw.labels,data:JSON.stringify({key:i.key,value:i.value()})}).fail(function(e){r.alertError(e,"Error saving label","Errors saving label for "+i.key+":<br>")}))}),e.when.apply(this,t).done(function(){r.growlAlert("Successfully saved labels!","success"),n.newLabels([]),n.reload()})}})});