package uy.edu.um.miniweb;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

	@GetMapping("/")
	public String home(Model model) {
		model.addAttribute("mensaje", "¡Spring Boot + Thymeleaf funcionando!");
		return "index"; // renderiza src/main/resources/templates/index.html
	}

}
