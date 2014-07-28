var requirejs = {
    paths: {
        'text': '../vendor/text',
        'jst': '../jst',
        'domReady': '../vendor/domReady',
        'jquery': '../vendor/jquery.min',
        'underscore': '../vendor/underscore',
        'backbone': '../vendor/backbone',
    },
    shims: {
        'underscore': {
            exports: '_'
        },
        'backbone': {
            deps: ['underscore'],
            exports: 'Backbone'
        },
    },
    waitSeconds: 0
};
