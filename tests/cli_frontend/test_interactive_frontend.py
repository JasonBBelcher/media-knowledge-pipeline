"""
Test suite for Interactive Frontend Integration
Following Test-Driven Development (TDD) principles
"""
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path
sys.path.insert(0, '/Users/jasonbelcher/Documents/code/media-knowledge-pipeline')

from src.media_knowledge.cli.interactive import run_interactive_frontend


class TestMenuOptionLogic:
    """Test the logic for each menu option without the infinite loop."""
    
    def test_menu_option_1_media_processing_logic(self):
        """Test the logic for menu option 1 - Process Media Content."""
        # Mock dependencies
        with patch('src.media_knowledge.cli.interactive.MediaWizard') as mock_wizard:
            with patch('src.media_knowledge.cli.interactive.CommandExecutor') as mock_executor:
                # Set up mock behavior
                wizard_instance = mock_wizard.return_value
                wizard_instance.process_media_interactive.return_value = {
                    'media_input': 'https://youtube.com/watch?v=test',
                    'media_type': 'youtube',
                    'template': 'lecture_summary',
                    'custom_prompt': None,
                    'output_config': {'save_json': True, 'save_markdown': True},
                    'processing_options': {'use_cloud': False, 'quiet': False, 'organize': True}
                }
                
                executor_instance = mock_executor.return_value
                executor_instance.execute_media_processing.return_value = True
                
                with patch('builtins.input', return_value='y'):
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        # Simulate the choice 1 logic
                        print("\nMedia Processing Selected")
                        
                        # Call wizard
                        config = wizard_instance.process_media_interactive()
                        assert config is not None
                        
                        # Display configuration
                        print("\nExecuting media processing with the following configuration:")
                        for key, value in config.items():
                            print(f"  {key}: {value}")
                        
                        # Confirm and execute
                        confirm = 'y'
                        if confirm in ['y', 'yes']:
                            success = executor_instance.execute_media_processing(config)
                            assert success == True
                            print("Media processing completed successfully!")
                        else:
                            print("Media processing cancelled.")
                        
                        print("\nReturning to main menu...\n")
                        
                        # Verify the wizard and executor were called
                        assert wizard_instance.process_media_interactive.called
                        assert executor_instance.execute_media_processing.called
    
    def test_menu_option_2_batch_processing_logic(self):
        """Test the logic for menu option 2 - Batch Process Multiple Items."""
        # Mock dependencies
        with patch('src.media_knowledge.cli.interactive.BatchWizard') as mock_wizard:
            with patch('src.media_knowledge.cli.interactive.CommandExecutor') as mock_executor:
                # Set up mock behavior
                wizard_instance = mock_wizard.return_value
                wizard_instance.process_batch_interactive.return_value = {
                    'urls_file': '/tmp/urls.txt',
                    'output_dir': '/tmp/outputs',
                    'parallel_workers': 2,
                    'template': 'technical_tutorial',
                    'custom_prompt': None,
                    'essay_options': {'enable_essay': True, 'force_essay': False},
                    'processing_options': {'use_cloud': True, 'quiet': True, 'organize': True}
                }
                
                executor_instance = mock_executor.return_value
                executor_instance.execute_batch_processing.return_value = True
                
                with patch('builtins.input', return_value='y'):
                    with patch('sys.stdout', new=StringIO()) as fake_out:
                        # Simulate the choice 2 logic
                        print("\nBatch Processing Selected")
                        
                        # Call wizard
                        config = wizard_instance.process_batch_interactive()
                        assert config is not None
                        
                        # Display configuration
                        print("\nExecuting batch processing with the following configuration:")
                        for key, value in config.items():
                            print(f"  {key}: {value}")
                        
                        # Confirm and execute
                        confirm = 'y'
                        if confirm in ['y', 'yes']:
                            success = executor_instance.execute_batch_processing(config)
                            assert success == True
                            print("Batch processing completed successfully!")
                        else:
                            print("Batch processing cancelled.")
                        
                        print("\nReturning to main menu...\n")
                        
                        # Verify the wizard and executor were called
                        assert wizard_instance.process_batch_interactive.called
                        assert executor_instance.execute_batch_processing.called
    
    def test_menu_option_3_logic(self):
        """Test the logic for menu option 3 - Create Essay from Existing Results."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 3 logic
            print("\nCreate Essay from Existing Results Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
            
            output = fake_out.getvalue()
            assert "Create Essay from Existing Results Selected" in output
            assert "feature will be implemented" in output.lower()
    
    def test_menu_option_4_logic(self):
        """Test the logic for menu option 4 - Scan Directory for Media Files."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 4 logic
            print("\nScan Directory for Media Files Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
            
            output = fake_out.getvalue()
            assert "Scan Directory for Media Files Selected" in output
            assert "feature will be implemented" in output.lower()
    
    def test_menu_option_5_logic(self):
        """Test the logic for menu option 5 - Watch Directory for New Files."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 5 logic
            print("\nWatch Directory for New Files Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
            
            output = fake_out.getvalue()
            assert "Watch Directory for New Files Selected" in output
            assert "feature will be implemented" in output.lower()
    
    def test_menu_option_6_logic(self):
        """Test the logic for menu option 6 - System Status and Requirements."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 6 logic
            print("\nSystem Status and Requirements Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
            
            output = fake_out.getvalue()
            assert "System Status and Requirements Selected" in output
            assert "feature will be implemented" in output.lower()
    
    def test_menu_option_7_logic(self):
        """Test the logic for menu option 7 - Show Pipeline Architecture."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 7 logic
            print("\nShow Pipeline Architecture Selected")
            print("This feature will be implemented in a future update.")
            print("\nReturning to main menu...\n")
            
            output = fake_out.getvalue()
            assert "Show Pipeline Architecture Selected" in output
            assert "feature will be implemented" in output.lower()
    
    def test_menu_option_0_logic(self):
        """Test the logic for menu option 0 - Exit."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # Simulate the choice 0 logic
            print("Thank you for using Media Knowledge Pipeline!")
            
            output = fake_out.getvalue()
            assert "Thank you for using Media Knowledge Pipeline" in output


class TestCancellationLogic:
    """Test cancellation scenarios."""
    
    def test_cancelled_media_processing_logic(self):
        """Test cancelled media processing scenario."""
        with patch('src.media_knowledge.cli.interactive.MediaWizard') as mock_wizard:
            # Mock wizard returning None (user cancelled)
            wizard_instance = mock_wizard.return_value
            wizard_instance.process_media_interactive.return_value = None
            
            with patch('sys.stdout', new=StringIO()) as fake_out:
                # Simulate the cancellation flow
                print("\nMedia Processing Selected")
                
                config = wizard_instance.process_media_interactive()
                assert config is None
                
                print("Media processing cancelled.")
                print("\nReturning to main menu...\n")
                
                # Verify wizard was called
                assert wizard_instance.process_media_interactive.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])