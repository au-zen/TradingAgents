import logging
import sys
import traceback
import datetime
import typer
from rich.console import Console
from rich.panel import Panel

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_selections.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

console = Console()
app = typer.Typer()

def create_question_box(title: str, prompt: str, default: str = None) -> Panel:
    """Create a question box with title and prompt."""
    box_content = f"[bold]{title}[/bold]\n"
    box_content += f"[dim]{prompt}[/dim]"
    if default:
        box_content += f"\n[dim]默认: {default}[/dim]"
    return Panel(box_content, border_style="blue", padding=(1, 2))

def get_stock_code() -> str:
    """Get stock code from user input with validation."""
    logger.info("Getting stock code input")
    console.print(create_question_box(
        "步骤1: 股票代码",
        "请输入要分析的A股代码（如603127.SH）",
        "603127.SH"
    ))
    
    stock_code = typer.prompt("", default="603127.SH")
    logger.info(f"Selected stock code: {stock_code}")
    return stock_code

def get_analysis_date() -> str:
    """Get analysis date from user input with validation."""
    logger.info("Getting analysis date")
    default_date = datetime.datetime.now().strftime("%Y-%m-%d")
    console.print(create_question_box(
        "步骤2: 分析日期",
        "请输入分析日期（YYYY-MM-DD）",
        default_date
    ))
    
    while True:
        try:
            date_str = typer.prompt("", default=default_date)
            analysis_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            
            if analysis_date.date() > datetime.datetime.now().date():
                console.print("[red]Error: Analysis date cannot be in the future[/red]")
                logger.warning("Invalid date: Future date entered")
                continue
                
            logger.info(f"Selected analysis date: {date_str}")
            return date_str
            
        except ValueError:
            console.print("[red]Error: Invalid date format. Please use YYYY-MM-DD[/red]")
            logger.error("Invalid date format entered")

def select_analysts() -> list:
    """Select analysts from predefined options."""
    logger.info("Selecting analysts")
    console.print(create_question_box("步骤3: 分析师团队", "请选择分析师类型"))
    
    analysts = ["market", "social", "news", "fundamentals"]
    logger.info(f"Selected analysts: {', '.join(analysts)}")
    console.print(f"[green]已选择分析师:[/green] {', '.join(analysts)}")
    return analysts

def select_research_depth() -> str:
    """Select research depth level."""
    logger.info("Selecting research depth")
    console.print(create_question_box("步骤4: 研究深度", "请选择研究深度等级"))
    
    depth = "Shallow - Quick research, few debate and strategy discussion rounds"
    logger.info(f"Selected research depth: {depth}")
    return depth

def select_llm_provider() -> tuple:
    """Select LLM provider and get backend URL."""
    logger.info("Selecting LLM provider")
    console.print(create_question_box("步骤5: LLM服务商", "请选择大模型服务"))
    
    provider = "Openrouter"
    url = "https://openrouter.ai/api/v1"
    logger.info(f"Selected LLM provider: {provider} with URL: {url}")
    console.print(f"You selected: {provider}        URL: {url}")
    return provider, url

def select_ai_models() -> tuple:
    """Select AI models for quick and deep thinking."""
    logger.info("Selecting AI models")
    console.print(create_question_box("步骤6: 智能体模型", "请选择用于分析的智能体模型"))
    
    quick_model = "DeepSeek V3 - 685B参数专家混合模型"
    deep_model = quick_model  # Using same model for both in this test
    logger.info(f"Selected models - Quick: {quick_model}, Deep: {deep_model}")
    return quick_model, deep_model

@app.command()
def main():
    """Run the test selection process."""
    try:
        logger.info("Starting test selection process")
        
        # Get stock code
        stock_code = get_stock_code()
        
        # Get analysis date
        analysis_date = get_analysis_date()
        
        # Select analysts
        analysts = select_analysts()
        
        # Select research depth
        research_depth = select_research_depth()
        
        # Select LLM provider
        llm_provider, backend_url = select_llm_provider()
        
        # Select AI models
        shallow_thinker, deep_thinker = select_ai_models()
        
        # Log final selections
        selections = {
            "ticker": stock_code,
            "analysis_date": analysis_date,
            "analysts": analysts,
            "research_depth": research_depth,
            "llm_provider": llm_provider.lower(),
            "backend_url": backend_url,
            "shallow_thinker": shallow_thinker,
            "deep_thinker": deep_thinker,
        }
        logger.info(f"Final selections: {selections}")
        
    except Exception as e:
        logger.error(f"Error during selection process: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    app()