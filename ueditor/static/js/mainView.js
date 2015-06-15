///**
// * 专利显示页的js代码
// * Created by abnerzheng on 15/4/21.
// */
//
angular.module('ui.bootstrap.demo', ['ui.bootstrap', 'ng.httpLoader']); //依赖注入，前端用了angular+bootstrap UI
angular.module('ui.bootstrap.demo').config(['httpMethodInterceptorProvider',
        function (httpMethodInterceptorProvider) {
            httpMethodInterceptorProvider.whitelistDomain('get_record_detail');
            httpMethodInterceptorProvider.whitelistDomain('get_infoAndArticle');
        }]
).controller('AccordionDemoCtrl', function ($scope, $http) {
        $scope.userName = "";
        $http.get('/getArticles').success(function (msg) {
            console.log(msg)
            $scope.userName = msg.name === "" ? "":msg.name + ",";
            $scope.articles = msg.articles;
            $scope.bigTotalItems = msg.count;
            $scope.totalItems = msg.count;
        });

        $scope.setPage = function (pageNo) {
            $scope.currentPage = pageNo; //选择页码
        };

        $scope.modify = function (id) {
            window.location.href = '/editor?article_id=' + id;
        }

        $scope.bigCurrentPage = 1; //目前分页所在页码
        $scope.bigTotalItems = 0; //总条目数

        $scope.pageChanged = function () {
            $http.get('/getArticles?page='+$scope.bigCurrentPage).success(function (msg) {
                console.log(msg);
                $scope.articles = msg.articles;
            })
        };

    })
