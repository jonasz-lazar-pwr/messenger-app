import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MessageStoreService {
  private messages: any[] = [];

  setMessages(newMessages: any[]): void {
    this.messages = [...newMessages];
  }

  getMessages(): any[] {
    return this.messages;
  }

  isNewMessageList(newList: any[]): boolean {
    if (this.messages.length !== newList.length) return true;
    const lastOld = this.messages[this.messages.length - 1];
    const lastNew = newList[newList.length - 1];
    return !lastOld || !lastNew || lastOld.id !== lastNew.id;
  }

  updateMessagesPreservingState(newMsgs: any[]): void {
    const existingMap = new Map(this.messages.map(msg => [msg.id, msg]));
    this.messages = newMsgs.map(newMsg => ({
      ...newMsg,
      loadFailed: existingMap.get(newMsg.id)?.loadFailed ?? false,
      loading: existingMap.get(newMsg.id)?.loading ?? true
    }));
  }
}
