webpackJsonp([8],{"/iT7":function(e,n){},"37t0":function(e,n){},"991W":function(e,n){},NHnr:function(e,n,t){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var o=t("7+uW"),a={render:function(){var e=this.$createElement;return(this._self._c||e)("router-view")},staticRenderFns:[]};var r=t("VU/8")({name:"App"},a,!1,function(e){t("/iT7")},null,null).exports,c=t("/ocq");o.default.use(c.a);var i=new c.a({routes:[{path:"/",name:"overview",component:function(e){return t.e(1).then(function(){var n=[t("sCCV")];e.apply(null,n)}.bind(this)).catch(t.oe)},redirect:{name:"overview"},children:[{path:"ldfs/",name:"ldfs",component:function(e){return t.e(0).then(function(){var n=[t("sSUJ")];e.apply(null,n)}.bind(this)).catch(t.oe)},redirect:{name:"overview"},children:[{path:"overview/",name:"overview",component:function(e){return t.e(5).then(function(){var n=[t("yQOy")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"disk/",name:"disk",component:function(e){return t.e(6).then(function(){var n=[t("ckg3")];e.apply(null,n)}.bind(this)).catch(t.oe)},redirect:{name:"manage"},children:[{path:"manage/",name:"manage",component:function(e){return t.e(4).then(function(){var n=[t("X+WY")];e.apply(null,n)}.bind(this)).catch(t.oe)}}]},{path:"region/",name:"region",component:function(e){return t.e(3).then(function(){var n=[t("FB7y")];e.apply(null,n)}.bind(this)).catch(t.oe)}},{path:"log/",name:"log",component:function(e){return t.e(2).then(function(){var n=[t("OZ6m")];e.apply(null,n)}.bind(this)).catch(t.oe)}}]}]}]}),u=t("zL8q"),p=t.n(u),l=(t("erWL"),t("q1nB")),s=t.n(l),f=(t("k5Zi"),t("991W"),t("ZphK"),t("37t0"),t("b79p"),t("//Fk")),d=t.n(f),h=t("mtWM"),m=t.n(h);Object({NODE_ENV:"production"}).API_ROOT,m.a.defaults.baseURL=Object({NODE_ENV:"production"}).API_ROOT,m.a.defaults.headers.post["Content-Type"]="application/x-www-fromurlencodeed",m.a.defaults.withCredentials=!0,m.a.interceptors.response.use(function(e){return e},function(e){if(e.response)switch(console.error(e.response),e.response.status){case 401:console.log(e.response.data.url),document.location=e.response.data.url}return d.a.reject(e.response.data)});var v=m.a,w=t("XLwt"),b=t.n(w);o.default.prototype.axios=v,o.default.prototype.echart=b.a,o.default.config.productionTip=!1,o.default.use(s.a),o.default.use(p.a),o.default.use(b.a);var y=new o.default({el:"#app",router:i,components:{App:r},template:"<App/>"});n.default=y},ZphK:function(e,n){},b79p:function(e,n){},erWL:function(e,n){},k5Zi:function(e,n){}},["NHnr"]);
//# sourceMappingURL=app.9e78ceee9e21921c8e2a.js.map