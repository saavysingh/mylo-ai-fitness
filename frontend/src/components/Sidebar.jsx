import React, { useState } from 'react';

const Sidebar = ({ isOpen, onToggle }) => {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}
      
      {/* Sidebar */}
      <div className={`
        fixed top-0 left-0 h-full bg-white shadow-lg z-50 transition-transform duration-300 ease-in-out
        ${isOpen ? 'translate-x-0' : '-translate-x-full'} 
        lg:translate-x-0 lg:static lg:shadow-none
        w-64
      `}>
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">M</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Mylo</h1>
                <p className="text-sm text-gray-600">Your AI Fitness Coach</p>
              </div>
            </div>
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 p-6">
            <ul className="space-y-2">
              <li>
                <a href="#" className="flex items-center space-x-3 px-3 py-2 rounded-lg bg-primary-50 text-primary-700 font-medium">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                  </svg>
                  <span>Home</span>
                </a>
              </li>
              <li>
                <a href="#" className="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 hover:text-gray-900 transition-colors">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>About</span>
                </a>
              </li>
            </ul>
          </nav>
          
          {/* Footer */}
          <div className="p-6 border-t border-gray-200">
            <div className="text-center text-sm text-gray-500">
              <p>Powered by AI</p>
              <p className="mt-1">Your personal fitness journey starts here</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar; 