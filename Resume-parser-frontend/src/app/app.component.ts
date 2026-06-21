import { Component, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { UploadComponent } from './components/upload/upload.component';
import { ResumeListComponent } from './components/resume-list/resume-list.component';
import { SearchComponent } from './components/search/search.component';
import { SkillQuestionsComponent } from './components/skill-questions/skill-questions.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, UploadComponent, ResumeListComponent, SearchComponent, SkillQuestionsComponent],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Resume Parser';
  activeTab: 'upload' | 'list' | 'search' | 'questions' = 'upload';
  isDarkMode = true;

  @ViewChild('tabsContainer') tabsContainer!: ElementRef;

  ngOnInit() {
    const savedTheme = localStorage.getItem('theme');
    this.isDarkMode = savedTheme ? savedTheme === 'dark' : true;
    this.updateTheme();
  }

  setActiveTab(tab: 'upload' | 'list' | 'search' | 'questions') {
    this.activeTab = tab;
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    this.updateTheme();
    localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
  }

  updateTheme() {
    document.documentElement.setAttribute('data-theme', this.isDarkMode ? 'dark' : 'light');
  }

  scrollTabs(offset: number) {
    if (this.tabsContainer) {
      this.tabsContainer.nativeElement.scrollBy({
        left: offset,
        behavior: 'smooth'
      });
    }
  }
}

