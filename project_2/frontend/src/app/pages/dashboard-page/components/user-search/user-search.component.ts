import { Component, EventEmitter, Output } from '@angular/core';
import { ChatService } from '../../../../services/chat.service';
import { Subject, debounceTime } from 'rxjs';


@Component({
  selector: 'app-user-search',
  standalone: false,
  templateUrl: './user-search.component.html',
  styleUrl: './user-search.component.css'
})
export class UserSearchComponent {
  query: string = '';
  results: any[] = [];
  searching: boolean = false;
  error: string = '';

  private queryChanged: Subject<string> = new Subject<string>();
  @Output() chatCreated = new EventEmitter<any>();

  constructor(private chatService: ChatService) {
    this.queryChanged.pipe(debounceTime(300)).subscribe((query) => {
      this.performSearch(query);
    });
  }

  onQueryChange(): void {
    this.queryChanged.next(this.query);
  }

  performSearch(query: string): void {
    this.error = '';
    if (!query.trim()) {
      this.results = [];
      return;
    }

    this.searching = true;
    this.chatService.searchUsers(query).subscribe({
      next: (users) => {
        this.results = users;
        this.searching = false;
      },
      error: () => {
        this.error = 'Failed to fetch users.';
        this.searching = false;
      }
    });
  }

  onCreateChat(user: any): void {
    this.chatService.createChat(user.sub).subscribe({
      next: (chat) => this.chatCreated.emit(chat),
      error: () => (this.error = 'Failed to create chat')
    });
  }

  getHighlightedParts(text: string): { value: string; match: boolean }[] {
    if (!this.query.trim()) return [{ value: text, match: false }];

    const escapedQuery = this.query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(escapedQuery, 'gi');
    const result: { value: string; match: boolean }[] = [];

    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = regex.exec(text)) !== null) {
      const start = match.index;
      const end = regex.lastIndex;

      if (start > lastIndex) {
        result.push({ value: text.slice(lastIndex, start), match: false });
      }

      result.push({ value: text.slice(start, end), match: true });
      lastIndex = end;
    }

    if (lastIndex < text.length) {
      result.push({ value: text.slice(lastIndex), match: false });
    }

    return result;
  }
}
