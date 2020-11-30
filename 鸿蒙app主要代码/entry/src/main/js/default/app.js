import storage from '@system.storage';
import router from '@system.router';
import file from '@system.file';
import request from '@system.request';
import fetch from '@system.fetch';
export default {
    onCreate() {
        console.info('AceApplication onCreate');
    },
    onDestroy() {
        console.info('AceApplication onDestroy');
    }
};
