import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardPageComponent } from './dashboard-page.component';
import { RouterModule, Routes } from '@angular/router';
import {FormsModule} from '@angular/forms';
import { ChatListComponent } from './components/chat-list/chat-list.component';
import { UserSearchComponent } from './components/user-search/user-search.component';
import { ChatWindowComponent } from './components/chat-window/chat-window.component';
import { MessageBubbleComponent } from './components/message-bubble/message-bubble.component';
import { MessageInputComponent } from './components/message-input/message-input.component';

const routes: Routes = [
  { path: '', component: DashboardPageComponent }
];

@NgModule({
  declarations: [
    DashboardPageComponent,
    ChatListComponent,
    UserSearchComponent,
    ChatWindowComponent,
    MessageBubbleComponent,
    MessageInputComponent
  ],
  imports: [CommonModule, RouterModule.forChild(routes), FormsModule],
  exports: [DashboardPageComponent]
})
export class DashboardPageModule { }
