#!/usr/bin/env python3
"""
SQLite Database Setup Script for Coding Questions Finder
"""

from app import app, db

def setup_database():
    """Create SQLite database and tables"""
    print("🚀 Setting up SQLite database for Coding Questions Finder...")
    print("=" * 60)
    
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if tables exist
            from app import User, QuestionSet
            
            # Test User table
            try:
                user_count = db.session.query(User).count()
                print(f"✅ User table ready (contains {user_count} users)")
            except Exception as e:
                print(f"⚠️  User table issue: {e}")
            
            # Test QuestionSet table
            try:
                question_count = db.session.query(QuestionSet).count()
                print(f"✅ QuestionSet table ready (contains {question_count} questions)")
            except Exception as e:
                print(f"⚠️  QuestionSet table issue: {e}")
                print("ℹ️  This is expected for the first run")
            
        print("\n🎉 SQLite database setup completed successfully!")
        print("📁 Database file: users.db (in instance folder)")
        print("🚀 You can now run: python app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    
    if success:
        print("\n✅ Setup completed! Your application is ready to use.")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
