var api = require('./api.js');
var async = require('async');

api.baseUrls['cms'] = 'http://studio.edx.ctlt.ubc.ca';
api.baseUrls['lms'] = 'http://edx.ctlt.ubc.ca';
//api.baseUrls['cms'] = 'http://localhost:8001';
//api.baseUrls['lms'] = 'http://localhost:8000';
var course_key = 'UBC/101/2015W1';
var xblock_prefix = 'i4x://UBC/101/ubcpi/';

var xblock_keys = [
    "d00d2132746245bdbb5c114c2d8b15f3",
    "7b966e2bafe143bc8215935674ae1648",
    "5a392cd1505e474c88b3ff268c3c1c19",
    "ecd249d85467422d91160cc3cb1265a8",
    "ffb8bfa3326b48ecad8b347e742b41a7",
    "bb14ec256582463c8236ee35e6c6aed3",
    "4c01fe998b6a41ff920cfe7ad69cd016",
    "9ea5086ab8b0487b89721bd6a25b5a50",
    "991e2ea40de742c7a9c1b48b3bd10e98",
    "236462479e4e46d995ebf6c1ecd76bab",
    "5d74b1b1f0fa4476a7aaa80f2f39c3ba",
    "cae410b7ca0c4b0f98e3ef3003e7ccff",
    "d5c2be98d6ce418bace95427d5281c73",
    "79d46111748d40acab70c69fffd2cb6c",
    "109bf534f14544debe20d5b127218178"
];

var original = [
    [0, 'This dog is anxious. She looks like the yellow dog that is anxious in the course material, hesitant and kind of unsure what is going on.'],
    [0, 'I think the dog is feeling anxiety. She just looks worried. Her front paw is kind of up. And she’s trying not to be noticed.'],
    [0, 'She is not moving toward whatever she’s looking at. Clearly, she is unsure and is watching with wide eyes what will happen next.'],
    [1, 'The dog is afraid! She is crouched protectively, backed up against a wall, and looks at something with "whale eyes".'],
    [1, 'I believe the dog is scared of something. Her ears are back, her eyes are wide (with the whites showing a little), and she is hunched over.'],
    [1, 'She is caught between flight and freeze. It seems she has escaped as far away as she could from something and is now trying to be still and small.'],
    [1, 'The reason I chose fear is because the dog is hiding and with a similar expression to the black dog in the course content.'],
    [2, 'This dog is feeling bad about something. I have seen this with my own dogs, when they hide from me and look guilty about something.'],
    [3, 'The dog appears to be frustrated with the person holding the camera. She is looking away from that person (and probably toward something she wants).'],
    [3, 'She is looking off at something and considering how to get at it. She looks about to spring into action, like she is just waiting for the right moment.']
];
var revised = [
    [0, 'This dog is anxious. She looks like the yellow dog that is anxious in the course material, hesitant and kind of unsure what is going on.'],
    [1, 'I think the dog is feeling anxiety. She just looks worried. Her front paw is kind of up. And she’s trying not to be noticed.'],
    [2, 'She is not moving toward whatever she’s looking at. Clearly, she is unsure and is watching with wide eyes what will happen next.'],
    [1, 'The dog is afraid! She is crouched protectively, backed up against a wall, and looks at something with "whale eyes".'],
    [1, 'I believe the dog is scared of something. Her ears are back, her eyes are wide (with the whites showing a little), and she is hunched over.'],
    [1, 'She is caught between flight and freeze. It seems she has escaped as far away as she could from something and is now trying to be still and small.'],
    [3, 'The reason I chose fear is because the dog is hiding and with a similar expression to the black dog in the course content.'],
    [2, 'This dog is feeling bad about something. I have seen this with my own dogs, when they hide from me and look guilty about something.'],
    [3, 'The dog appears to be frustrated with the person holding the camera. She is looking away from that person (and probably toward something she wants).'],
    [3, 'She is looking off at something and considering how to get at it. She looks about to spring into action, like she is just waiting for the right moment.']
];

async.timesSeries(original.length, function(i, next) {
    async.timesSeries(xblock_keys.length, function(j, nextx) {
        async.series([
            function (cb) {
                api.createUserOrLogin('pitestuser'+i, 'lms', course_key, cb);
            },
            function (cb) {
                api.piSubmitAnswer(course_key, xblock_prefix + xblock_keys[j], {
                    q: original[i][0],
                    rationale: original[i][1],
                    status: 0
                }, cb);
            },
            function (cb) {
                api.piSubmitAnswer(course_key, xblock_prefix + xblock_keys[j], {
                    q: revised[i][0],
                    rationale: revised[i][1],
                    status: 1
                }, cb);
            }
        ], function (err, results) {
            nextx(err, results);
        });
    }, function(err, results) {
       next(err, results);
    });
});
