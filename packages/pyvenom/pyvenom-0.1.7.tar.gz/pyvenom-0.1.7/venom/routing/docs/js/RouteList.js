'use strict';
(function (root) {
  
  function RouteList (docContent) {
    this.init(docContent);
  }
  
  RouteList.prototype = {
    init: function (docContent) {
      // Cache all the elements first on the instance 
      this.$list = $('.js-RouteList');
      
      this.docContent = docContent;
      this.routes = [];
      this.activeRoute = null;

      this.bindEvents();
      this.refresh();
    },
    bindEvents: function () {
      
    },
    refresh: function () {
      fetch('/routes/v{{version}}').then(function(response){
        return response.json();
      }).then(this.createRoutes.bind(this))
    },
    createRoutes: function (json) {
      this.clearRoutes();
      
      var routes = json.routes;
      for(var i=0,route; route=routes[i++];){
        for(var j=0,method; method=route.methods[j++];){
          var newRoute = new Route(this, route.path, method);
          this.routes.push(newRoute);
        }
      }
      
      this.applyRoutes()
    },
    clearRoutes: function () {
      for(var i=0,route; route=this.routes[i++];){
        this.$list.removeChild(route.$elem);
      }
      
      this.routes = [];
    },
    applyRoutes: function () {
      for(var i=0,route; route=this.routes[i++];){
        this.$list.appendChild(route.$elem);
      }
    },
    triggerActivateRoute: function (route) {
      if(!!this.activeRoute)
        this.activeRoute.triggerDeactivate();
      route.triggerActivate();
      this.activeRoute = route;
    }
  };
  
  root.RouteList = RouteList;
  
})(window);