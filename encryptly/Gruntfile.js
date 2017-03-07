module.exports = function (grunt) {
    grunt.initConfig({
        combine_mq: {
            new_filename: {
                options: {
                    beautify: true
                },
                src: 'static/css/encryptly.css',
                dest: 'static/css/encryptly.css'
            }
        }
    });
    grunt.loadNpmTasks('grunt-combine-mq');
    grunt.registerTask('default', 'combine_mq');
};