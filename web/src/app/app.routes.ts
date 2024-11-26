import { Routes } from '@angular/router';
import {
    HomePageComponent,
    TaskDetailPageComponent,
    TaskListPageComponent,
} from './pages';

export const routes: Routes = [
    {
        path: '',
        component: HomePageComponent,
    },

    {
        path: 'tasks',
        component: TaskListPageComponent,
    },

    {
        path: 'tasks/:id',
        component: TaskDetailPageComponent,
    },
];
